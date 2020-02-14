from rest_framework import serializers

from apps.workspaces.models import (
    Environment,
    Flow,
    FunctionFile,
    Integration,
    Workspace,
    Release,
    WorkspaceRelease,
    EnvironmentRelease,
    FunctionFileRelease,
    IntegrationRelease
)


class WorkspaceSerializer(serializers.ModelSerializer):
    workspace_color = serializers.CharField(required=False)

    class Meta:
        model = Workspace
        fields = "__all__"


class EnvironmentSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    environment_variables = serializers.JSONField(required=False)

    class Meta:
        model = Environment
        fields = "__all__"


class IntegrationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    integration_variables = serializers.JSONField(required=False)

    class Meta:
        model = Integration
        fields = "__all__"


class FunctionFileSerializer(serializers.ModelSerializer):
    function_data = serializers.JSONField(required=False)

    class Meta:
        model = FunctionFile
        fields = "__all__"


class FlowSerializer(serializers.ModelSerializer):
    flow_layout = serializers.JSONField(required=False)
    flow_data = serializers.JSONField(required=False)

    class Meta:
        model = Flow
        fields = "__all__"



class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = "__all__"

    def create(self, validated_data):
        release = Release.objects.create(**validated_data)
        
        workspace_release = release.workspace.__dict__
        workspace_release["workspace"] = release.workspace
        workspace_release["release"] = release
        del workspace_release["id"]
        workspace_release = WorkspaceRelease.objects.create(**workspace_release)

        # environments_release = workspace.environment_set.all()
        # for environment in environments_release:
        #     environment_rel = environment.__dict__
        #     environment_rel["workspace_release"] = workspace_release
        #     environment_rel["release"] = release
        #     environment_rel["environment"] = environment
        #     del environment_rel["id"]
        #     environment = EnvironmentRelease.objects.create(**environment_rel)
        

        # integrations_release = workspace.integration_set.all()
        # for integration in integrations_release:
        #     integration_rel = integration.__dict__
        #     integration_rel["workspace_release"] = workspace_release
        #     integration_rel["release"] = release
        #     integration_rel["integration"] = integration
        #     del integration_rel["id"]
        #     integration = IntegrationRelease.objects.create(**integration_rel)


        # function_files_release = workspace.functionfile_set.all()
        # for function_file in function_files_release:
        #     function_file_rel = function_file.__dict__
        #     function_file_rel["workspace_release"] = workspace_release
        #     function_file_rel["release"] = release
        #     function_file_rel["function_file"] = function_file
        #     del function_file_rel["id"]
        #     function_file = function_fileRelease.objects.create(**function_file_rel)

        return release

