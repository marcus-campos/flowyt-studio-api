from rest_framework import generics, mixins, status, viewsets, permissions
from apps.hosts.models import Host
from . import serializers
from apps.workspaces.permissions import IsInTeamPermission


class HostViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet,
):

    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.HostSerializer
    queryset = Host.objects.all()


class HostDetailViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):

    permission_classes = (
        IsInTeamPermission,
        permissions.IsAdminUser,
    )
    serializer_class = serializers.HostSerializer
    queryset = Host.objects.all()
