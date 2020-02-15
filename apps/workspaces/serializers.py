from rest_framework import serializers

from apps.workspaces.models import (Environment, EnvironmentRelease, Flow,
                                    FlowRelease, FunctionFile,
                                    FunctionFileRelease, Integration,
                                    IntegrationRelease, Release, Route,
                                    Workspace, WorkspaceRelease, RouteRelease)


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

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
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

        # Flows
        flows_release = release.workspace.flow_set.all()
        for flow in flows_release:
            flow_rel = FlowRelease()

            flow_rel.workspace_release = workspace_release
            flow_rel.release = release
            flow_rel.flow = flow

            flow_rel.name = flow.name
            flow_rel.description = flow.description
            flow_rel.flow_layout = flow.flow_layout
            flow_rel.flow_data = flow.flow_data
           
            flow_rel.save()


        # Routes
        routes_release = release.workspace.route_set.all()
        for route in routes_release:
            route_rel = RouteRelease()

            route_rel.workspace_release = workspace_release
            route_rel.flow_release = route.flow_release
            route_rel.release = release
            route_rel.route = route

            route_rel.path = route.path
            route_rel.description = route.description
            route_rel.method = route.method
            route_rel.active = route.active
           
            route_rel.save()
        
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


class PublishSerializer(serializers.Serializer):
    release = serializers.UUIDField(required=True)
    environments = serializers.ListField(required=True)

    def validate(self, data):
        try:
            release = Release.objects.get(pk=str(data["release"]))
            data["release"] = release
        except Release.DoesNotExist:
            raise serializers.ValidationError("This release does not exist")

        for index in range(len(data["environments"])):
            try:
                environment = Environment.objects.get(pk=data["environments"][index])
                data["environments"][index] = environment
            except Environment.DoesNotExist:
                raise serializers.ValidationError("The environment {0} does not exist".format(data["environments"][index]))

        return data
