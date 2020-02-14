import copy
import json

from django.core import serializers
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.workspaces.models import (Environment, Flow, FunctionFile,
                                    Integration, Workspace, Release)
from apps.workspaces.serializers import (EnvironmentSerializer, FlowSerializer,
                                         FunctionFileSerializer,
                                         IntegrationSerializer,
                                         ReleaseSerializer,
                                         WorkspaceSerializer)


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


class ReleaseViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Release.objects.all()
    serializer_class = FlowSerializer
    filter_fields = ("workspace__id",)


class ReleaseView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     generics.GenericAPIView):
    serializer_class = ReleaseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["workspace"] = kwargs["id"]

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        release = serializer.create(serializer.validated_data)
        serialized_release = serializers.serialize('python', [release])[0]
        serialized_release["fields"]["id"] = serialized_release["pk"]

        return Response(data=serialized_release["fields"], status=200)
