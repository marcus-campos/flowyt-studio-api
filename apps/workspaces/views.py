import copy
import json
import shutil
import os

import requests
from apps.teams.models import Team
from apps.workspaces.models import (
    Environment,
    Flow,
    FunctionFile,
    Integration,
    Release,
    Route,
    Workspace,
    WorkspaceRelease,
)
from apps.workspaces.permissions import IsCreatorPermission, IsInTeamPermission
from apps.workspaces.serializers import (
    EnvironmentSerializer,
    FlowSerializer,
    FunctionFileSerializer,
    IntegrationSerializer,
    PublishSerializer,
    ReleaseSerializer,
    RouteSerializer,
    WorkspaceSerializer,
)
from apps.workspaces.services import ConfigTranslation, FlowTranslation, ReleaseBuilder
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from orchestryzi_api.settings import ENGINE_ENDPOINTS, WORKSPACE_PUBLISH_MODE
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from utils.models import to_dict
from utils.redis import redis

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = (IsInTeamPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        teams = Team.objects.filter(members__in=[self.request.user])
        return queryset.filter(team__in=teams)


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsInTeamPermission,)

    def perform_destroy(self, instance):
        if not instance.can_delete:
            raise PermissionDenied(detail="The default debug environment cant be removed")
        return super(EnvironmentViewSet, self).perform_destroy(instance)


class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsInTeamPermission,)


class FunctionFileViewSet(viewsets.ModelViewSet):
    queryset = FunctionFile.objects.all()
    serializer_class = FunctionFileSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsInTeamPermission,)


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsInTeamPermission,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_fields = ("flow__id", "workspace__id")
    permission_classes = (IsInTeamPermission,)


class ReleaseViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsCreatorPermission,)

    def retrieve(self, request, *args, **kwargs):
        release = self.queryset.get(pk=kwargs["pk"])
        response = to_dict(release)
        response["environments"] = []
        for release in release.environmentrelease_set.all():
            environment = to_dict(release)
            response["environments"].append(
                {
                    "id": environment["id"],
                    "name": environment["name"],
                    "description": environment["description"],
                    "created_at": environment["created_at"],
                    "updated_at": environment["updated_at"],
                }
            )
        return Response(data=response, status=200)


class ReleaseView(generics.GenericAPIView):
    serializer_class = ReleaseSerializer
    permission_classes = (IsInTeamPermission,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["workspace"] = kwargs["id"]

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        release = serializer.create(serializer.validated_data)
        serialized_release = serializers.serialize("python", [release])[0]
        serialized_release["fields"]["id"] = serialized_release["pk"]

        return Response(data=serialized_release["fields"], status=200)


class ReleasePublishView(generics.GenericAPIView):
    serializer_class = PublishSerializer
    permission_classes = (IsInTeamPermission,)

    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["release"] = kwargs["id"]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # try:
        # Make
        projects_to_publish = self._make_workspaces(serializer.validated_data)

        # Publish
        has_errors = self._publish(projects_to_publish, serializer.validated_data["host"])

        # Response
        response = {"msg": "The projects were published successfully!"}
        
        if WORKSPACE_PUBLISH_MODE == "upload":
            # Delete release files
            self._delete_release_files(projects_to_publish)

            # Prepare response
            urls = [
                "{0}/{1}".format(serializer.validated_data["host"].host, project["name"])
                for project in projects_to_publish["projects"]
            ]
            
            response = {"msg": "The projects were published successfully!", "urls": urls}

        # except:
        #     response = {
        #         "msg": "It was not possible to generate a build for this release. Check that there is no incomplete data and create a new release."
        #     }
        #     return Response(data=response, status=400)

        if has_errors:
            response = {"msg": "Something went wrong! This release could not be published."}
            return Response(data=response, status=400)

        return Response(data=response, status=200)

    def _make_workspaces(self, validated_data):
        release = validated_data["release"]
        workspace = WorkspaceRelease.objects.get(release=release)
        flows = workspace.flowrelease_set.all()
        routes = workspace.routerelease_set.all()
        integrations = workspace.integrationrelease_set.all()
        function_files = workspace.functionfilerelease_set.all()

        return ReleaseBuilder().make(
            validated_data, release, workspace, flows, routes, integrations, function_files
        )

    def _publish(self, projects, host):
        url_publish = "{0}{1}".format(host.host, ENGINE_ENDPOINTS["publish"])
        url_reload = "{0}{1}".format(host.host, ENGINE_ENDPOINTS["reload"])
        has_errors = False

        if WORKSPACE_PUBLISH_MODE == "upload":
            for project_zip in projects["projects_zips"]:
                if not has_errors:
                    result = requests.post(
                        url_publish,
                        files={"workpace_zip_file": ("{0}.zip".format(project_zip["name"]), project_zip["file"])},
                        headers={"X-Orchestryzi-Token": host.secret_token},
                    )

                    if result.status_code != 200:
                        has_errors = True

            result = requests.get(url_reload, headers={"X-Orchestryzi-Token": host.secret_token})

        elif WORKSPACE_PUBLISH_MODE == "redis":
            for project in projects:
                project_key = project["name"] #TODO: Set subdomain
                redis.set(project_key, json.dumps(project["data"]))

        return has_errors

    def _delete_release_files(self, projects):
        try:
            for project in projects["projects"]:
                shutil.rmtree(project["project_folder"])
                os.remove("{0}.zip".format(project["project_folder"]))
            return True
        except:
            return False

    def _transform_redis(self, projects_to_publish):
        projects = []
        base_model = {
            "config": {},
            "flows": {},
            "functions": {},
            "routes": []
        }

        for project in projects_to_publish:
            model = copy.deepcopy(base_model)

            model["routes"] = project["data"]["routes"]
            model["config"] = {config["name"]: json.loads(config["data"]) for config in project["data"]["config"]}
            model["flows"] = {flow["name"]: json.loads(flow["data"]) for flow in project["data"]["flows"]}
            model["functions"] = project["data"]["function"]
            
            projects.append({
                "name": project["name"],
                "data": model
            })

        return projects
