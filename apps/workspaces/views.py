import copy
import os
import shutil
import json

from django.core import serializers
from django.db.models import Q
from django.utils.text import slugify
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

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
from apps.workspaces.services import ConfigTranslation, FlowTranslation
from orchestryzi_api.settings import BASE_DIR
from utils.models import to_dict


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = (IsInTeamPermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        teams = Team.objects.filter(members__in=[self.request.user])
        return queryset.filter(team__in=teams)


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_fields = ("workspace__id",)
    permission_classes = (IsInTeamPermission,)


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
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
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

        self.__make_workspaces(serializer.validated_data)

        return Response(data={}, status=200)

    def __make_workspaces(self, validated_data):
        release = validated_data["release"]
        workspace = WorkspaceRelease.objects.get(release=release)
        flows = workspace.flowrelease_set.all()
        routes = workspace.routerelease_set.all()
        integrations = workspace.integrationrelease_set.all()
        function_files = workspace.functionfilerelease_set.all()

        environments_to_publish = validated_data["environments"]

        project_structure = {"config": [], "flows": [], "functions": [], "routes": []}

        projects_to_publish = []

        for environment in environments_to_publish:
            project = copy.deepcopy(project_structure)

            slug = slugify("{0}-{1}".format(workspace.name, environment.name))

            # Configs
            project["config"].append(
                {
                    "name": "settings",
                    "data": json.dumps(
                        self.__config_settings(
                            release, workspace, environment, integrations
                        )
                    ),
                }
            )

            # Flows and Routes
            flows_list = []
            for flow in flows:
                slug = slugify(flow.name)
                flow_id = str(flow.id)
                
                flows_list.append({"name": slug, "data": json.dumps(FlowTranslation().translate(flow))})
                
            project["flows"] = flows_list
            

            # Routes
            for route in routes:
                project["routes"].append(
                    {
                        "path": route.path,
                        "method": route.method,
                        "flow": slugify(route.flow_release.name)
                    }
                )

            # Functions
            for function in function_files:
                project["functions"].append(
                    {"name": function.name.lower(), "data": function.function_data}
                )

            projects_to_publish.append({"name": slug, "data": project})

        self.__create_project_and_zip(projects_to_publish)

    def __create_project_and_zip(self, projects):
        for project in projects:
            self.__create_project_file(project, "config", "json")
            self.__create_project_file(project, "flows", "json")
            self.__create_project_file(project, "functions", "py")
            self.__create_project_file(project, "routes", "json")

    def __create_project_file(self, project, key, extension):
        WORKSPACE_DIR = BASE_DIR + "/storage/tmp/workspaces/"
        project_folder = WORKSPACE_DIR + project["name"]

        if key == "routes":
            file = open("{0}/{1}.{2}".format(project_folder, key, extension), "w+")
            file.write(json.dumps(project["data"]["routes"]))
            file.close()
            return

        if os.path.exists(project_folder+"/{0}".format(key)):
            shutil.rmtree(project_folder+"/{0}".format(key))
        os.makedirs(project_folder+"/{0}".format(key))

        for item in project["data"][key]:
            file = open(
                "{0}/{1}/{2}.{3}".format(project_folder, key, item["name"], extension),
                "w+",
            )
            file.write(item["data"])
            file.close()

    def __config_settings(self, release, workspace, environment, integrations):
        config_settings = ConfigTranslation().settings_translate(
            release, workspace, environment, integrations
        )
        return config_settings

    def __flows(self, flows):
        flows_list = []
        for flow in flows:
            slug = slugify(flow.name)
            flows_list.append(
                {"name": slug, "data": json.dumps(FlowTranslation().translate(flow))}
            )
        return flows_list
