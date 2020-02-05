from rest_framework import viewsets

from apps.workspaces.models import Workspace, Flow
from apps.workspaces.serializers import WorkspaceSerializer, FlowSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
