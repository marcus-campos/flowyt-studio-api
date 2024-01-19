from rest_framework import generics, mixins, permissions, status, viewsets

from apps.hosts.models import Host

from ..teams.models import Team
from . import serializers
from .permissions import IsInHostTeamMemberPermission


class HostViewSet(generics.ListAPIView):
    serializer_class = serializers.HostSerializer

    def get_queryset(self):
        teams_id = Team.objects.filter(members__in=[self.request.user]).values_list("id", flat=True)
        queryset = Host.objects.filter(team__id__in=teams_id)
        return queryset


class HostDetailViewSet(generics.RetrieveAPIView):
    permission_classes = (IsInHostTeamMemberPermission,)
    serializer_class = serializers.HostSerializer
    queryset = Host.objects.all()
