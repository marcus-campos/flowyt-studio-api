from rest_framework import serializers

from apps.workspaces.models import Workspace, Flow


class WorkspaceSerializer(serializers.ModelSerializer):
    envs = serializers.JSONField(required=False)
    integrations = serializers.JSONField(required=False)

    class Meta:
        model = Workspace
        fields = "__all__"


class FlowSerializer(serializers.ModelSerializer):
    envs = serializers.JSONField(required=False)
    integrations = serializers.JSONField(required=False)

    class Meta:
        model = Flow
        fields = "__all__"
