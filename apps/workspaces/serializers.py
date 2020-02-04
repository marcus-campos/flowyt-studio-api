from rest_framework import serializers

from apps.workspaces.models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    envs = serializers.JSONField(required=False)

    class Meta:
        model = Workspace
        fields = (
            "id",
            "name",
            "description",
            "slug",
            "integrations",
            "envs",
            "created_at",
            "updated_at",
        )
