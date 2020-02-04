from rest_framework import viewsets

from apps.workspaces.models import Workspace
from apps.workspaces.serializers import WorkspaceSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer


