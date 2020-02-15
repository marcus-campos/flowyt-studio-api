import copy
import json

from django.core import serializers
from django.utils.text import slugify
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.workspaces.models import (Environment, Flow, FunctionFile,
                                    Integration, Release, Route, Workspace,
                                    WorkspaceRelease)
from apps.workspaces.serializers import (EnvironmentSerializer, FlowSerializer,
                                         FunctionFileSerializer,
                                         IntegrationSerializer,
                                         PublishSerializer, ReleaseSerializer,
                                         RouteSerializer, WorkspaceSerializer)
from apps.workspaces.services import ConfigTranslation, FlowTranslation


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_fields = ("workspace__id",)


class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    filter_fields = ("workspace__id",)


class FunctionFileViewSet(viewsets.ModelViewSet):
    queryset = FunctionFile.objects.all()
    serializer_class = FunctionFileSerializer
    filter_fields = ("workspace__id",)


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    filter_fields = ("workspace__id",)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_fields = ("flow__id", "workspace__id")

class ReleaseViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Release.objects.all()
    serializer_class = FlowSerializer
    filter_fields = ("workspace__id",)


class ReleaseView(generics.GenericAPIView):
    serializer_class = ReleaseSerializer

    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["workspace"] = kwargs["id"]

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        release = serializer.create(serializer.validated_data)
        serialized_release = serializers.serialize('python', [release])[0]
        serialized_release["fields"]["id"] = serialized_release["pk"]

        return Response(data=serialized_release["fields"], status=200)

class ReleasePublishView(generics.GenericAPIView):
    serializer_class = PublishSerializer
    
    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["release"] = kwargs["id"]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
    
        self.__run(serializer.validated_data)

        return Response(data={}, status=200)


    def __run(self, validated_data):
        release = validated_data["release"]
        workspace = WorkspaceRelease.objects.get(release=release)
        flows = workspace.flowrelease_set.all()
        integrations = workspace.integrationrelease_set.all()
        function_files = workspace.functionfilerelease_set.all()

        environments_to_publish = validated_data["environments"]

        slug = ""
        config_settings = {}
        flows_list = []

        for environment in environments_to_publish:
            slug = slugify("{0}-{1}".format(workspace.name, environment.name))
            config_settings = self.__config_settings(release, workspace, environment, integrations)
            
            flows_list = self.__flows(flows)
    
        pass

    def __config_settings(self, release, workspace, environment, integrations):
        config_settings = ConfigTranslation().settings_translate(release, workspace,
                                                                 environment, integrations)
        return config_settings


    def __flows(self, flows):
        flows_list = []
        for flow in flows:
            flows_list.append(
                FlowTranslation().translate(flow)
            )
        return flows_list
