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

    def validate(self, data):
        release = Release.objects.filter(name__exact=data["name"], workspace=data["workspace"])

        if release.exists():
            raise serializers.ValidationError("There is already a release with this name")

        return data

    def create(self, validated_data):
        release = Release.objects.create(**validated_data)
        
        # Workspaces
        workspace_release = WorkspaceRelease()
        workspace_release.workspace = release.workspace
        workspace_release.release = release

        workspace_release.name = release.workspace.name
        workspace_release.description = release.workspace.description
        workspace_release.slug = release.workspace.slug
        workspace_release.workspace_color = release.workspace.workspace_color

        workspace_release.save()
        
        # Environments
        environments_release = release.workspace.environment_set.all()
        for environment in environments_release:
            environment_rel = EnvironmentRelease()

            environment_rel.workspace_release = workspace_release
            environment_rel.release = release
            environment_rel.environment = environment

            environment_rel.name = environment.name
            environment_rel.description = environment.description
            environment_rel.environment_variables = environment.environment_variables
           
            environment_rel.save()
        

        # Integrations
        integrations_release = release.workspace.integration_set.all()
        for integration in integrations_release:
            integration_rel = IntegrationRelease()

            integration_rel.workspace_release = workspace_release
            integration_rel.release = release
            integration_rel.integration = integration

            integration_rel.name = integration.name
            integration_rel.description = integration.description
            integration_rel.integration_variables = integration.integration_variables
            
            integration_rel.save()


        # Function file
        function_files_release = release.workspace.functionfile_set.all()
        for function_file in function_files_release:
            function_file_rel = FunctionFileRelease()

            function_file_rel.workspace_release = workspace_release
            function_file_rel.release = release
            function_file_rel.function_file = function_file

            function_file_rel.name = function_file.name
            function_file_rel.description = function_file.description
            function_file_rel.function_data = function_file.function_data

            function_file_rel.save()

        return release

