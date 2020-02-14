import copy

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.workspaces.models import (Environment, Flow, FunctionFile,
                                    Integration, Workspace)
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


class ReleaseView(generics.GenericAPIView):
    serializer_class = ReleaseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data["workspace"] = kwargs["id"]

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        release = serializer.create(serializer.validated_data)

        return Response(data=release, status=200)
