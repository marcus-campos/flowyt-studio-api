from rest_framework import viewsets

from apps.workspaces.models import Flow, Workspace
from apps.workspaces.serializers import (
    EnvironmentSerializer,
    FlowSerializer,
    FunctionFileSerializer,
    IntegrationSerializer,
    WorkspaceSerializer,
)


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = EnvironmentSerializer


class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = IntegrationSerializer


class FunctionFileViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FunctionFileSerializer


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
