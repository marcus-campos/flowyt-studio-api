from rest_framework import serializers
from apps.hosts.models import Host


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = "__all__"
