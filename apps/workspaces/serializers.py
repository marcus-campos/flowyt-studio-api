from rest_framework import serializers

from apps.teams.models import Team
from apps.workspaces.models import (
    Environment,
    EnvironmentRelease,
    Flow,
    FlowRelease,
    FunctionFile,
    FunctionFileRelease,
    Integration,
    IntegrationRelease,
    Release,
    Route,
    Workspace,
    WorkspaceRelease,
    RouteRelease,
)


class WorkspaceSerializer(serializers.ModelSerializer):
    workspace_color = serializers.CharField(required=False)

    class Meta:
        model = Workspace
        fields = "__all__"
        read_only_fields = ["creator"]

    def validate(self, data):
        creator = self.context.get("user", None)
        if not creator:
            raise serializers.ValidationError("User not found.")
        if not Team.objects.filter(members__in=[creator]).exists():
            raise serializers.ValidationError("User is not in the specified Team.")
        return data


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

    workspace_release = None
    release = None

    class Meta:
        model = Release
        fields = "__all__"

    def validate(self, data):
        release = Release.objects.filter(name__exact=data["name"], workspace=data["workspace"])

        if release.exists():
            raise serializers.ValidationError("There is already a release with this name")

        return data

    def create(self, validated_data):
        self.release = Release.objects.create(**validated_data)

        # Workspaces

        self.workspace_release = WorkspaceRelease()
        self.workspace_release.name = self.release.workspace.name
        self.workspace_release.description = self.release.workspace.description
        self.workspace_release.workspace_color = self.release.workspace.workspace_color
        self.workspace_release.save()

        # Flows
        flows_release = self.release.workspace.flow_set.all()
        self._create_release_copies(
            FlowRelease, flows_release, ["name", "description", "flow_layout", "flow_data"],
        )

        # Routes
        routes_release = self.release.workspace.route_set.all()
        for route in routes_release:
            self._copy_model_instance(
                RouteRelease,
                route,
                ["path", "description", "method", "active"],
                {"flow_release": route.flow.flowrelease_set.all().first()},
            )

        # Environments
        environments_release = self.release.workspace.environment_set.all()
        self._create_release_copies(
            EnvironmentRelease, environments_release, ["name", "description", "environment_variables"],
        )

        # Integrations
        integrations_release = self.release.workspace.integration_set.all()
        self._create_release_copies(
            IntegrationRelease, integrations_release, ["name", "description", "integration_variables"],
        )

        # Function file
        function_files_release = self.release.workspace.functionfile_set.all()
        self._create_release_copies(
            FunctionFileRelease, function_files_release, ["name", "description", "function_data"],
        )

        return self.release

    def _create_release_copies(self, model_class, sources, copy=[]):
        for source in sources:
            self._copy_model_instance(
                model_class, source, copy,
            )

    def _copy_model_instance(self, model_class, instance, copy=[], add={}):
        rel_instance = model_class()
        for field in copy:
            setattr(rel_instance, field, getattr(instance, field))
        for field, value in add.items():
            setattr(rel_instance, field, value)

        instance_attr_name = instance.__class__.__name__.lower()
        setattr(rel_instance, instance_attr_name, instance)

        rel_instance.workspace_release = self.workspace_release
        rel_instance.release = self.release
        rel_instance.save()
        return rel_instance


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
                raise serializers.ValidationError(
                    "The environment {0} does not exist".format(data["environments"][index])
                )

        return data
