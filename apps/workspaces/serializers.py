import json

from apps.hosts.models import Host
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
    RouteRelease,
    Workspace,
    WorkspaceRelease,
    Language,
)
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "language"]


class WorkspaceSerializer(serializers.ModelSerializer):
    workspace_color = serializers.CharField(required=False)

    class Meta:
        model = Workspace
        fields = "__all__"
        read_only_fields = ["creator"]

    def validate(self, data):
        creator = self.context.get("user", None)
        if self.instance:
            creator = self.instance.creator
        if not creator:
            raise serializers.ValidationError("User not found.")
        if not Team.objects.filter(members__in=[creator]).exists():
            raise serializers.ValidationError("User is not in the specified Team.")
        return data

    def create(self, validated_data):
        workspace = super(WorkspaceSerializer, self).create(validated_data)
        debug_env = Environment()
        debug_env.name = "debug"
        debug_env.description = "Debug Environment"
        debug_env.workspace = workspace
        debug_env.can_delete = False
        debug_env.debug = True
        debug_env.safe_mode = json.dumps({"enable": True, "safe_time": 10}, ensure_ascii=False)
        debug_env.save()

        return workspace


class EnvironmentSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    environment_variables = serializers.JSONField(required=False)

    class Meta:
        model = Environment
        exclude = ["can_delete"]

    def create(self, validated_data):
        validated_data["safe_mode"] = json.dumps({"enable": True, "safe_time": 10}, ensure_ascii=False)
        workspace = super(EnvironmentSerializer, self).create(validated_data)

        return workspace


class IntegrationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    integration_variables = serializers.JSONField(required=False)

    class Meta:
        model = Integration
        fields = "__all__"


class FunctionFileSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        self.release = Release.objects.create(**validated_data)

        # Workspaces
        self.workspace_release = WorkspaceRelease.objects.create(
            name=self.release.workspace.name,
            description=self.release.workspace.description,
            workspace_color=self.release.workspace.workspace_color,
            release=self.release,
        )
        # Flows
        self._create_release_copies(
            Flow, FlowRelease, ["flow_layout", "flow_data"],
        )
        # Environments
        self._create_release_copies(
            Environment, EnvironmentRelease, ["environment_variables", "debug", "safe_mode"],
        )
        # Integrations
        self._create_release_copies(
            Integration, IntegrationRelease, ["integration_variables"],
        )
        # Function file
        self._create_release_copies(
            FunctionFile, FunctionFileRelease, ["function_data"],
        )
        # Routes
        self._create_route_copies()

        return self.release

    def _create_route_copies(self):
        routes_release = self.release.workspace.route_set.all()
        for route in routes_release:
            self._copy_model_instance(
                RouteRelease,
                route,
                ["path", "description", "method", "active"],
                {"flow_release": route.flow.flowrelease_set.all().first()},
            )

    def _create_release_copies(self, from_class, to_class, extra=[]):
        instance_attr_name = "{0}_set".format(from_class.__name__.lower())
        sources = getattr(self.release.workspace, instance_attr_name).all()
        for from_instance in sources:
            self._copy_model_instance(
                to_class, from_instance, extra + ["name", "description"],
            )

    def _copy_model_instance(self, model_class, from_instance, copy=[], add={}):
        rel_instance = model_class()
        for field in copy:
            setattr(rel_instance, field, getattr(from_instance, field))
        for field, value in add.items():
            setattr(rel_instance, field, value)

        instance_attr_name = from_instance.__class__.__name__.lower()
        setattr(rel_instance, instance_attr_name, from_instance)

        rel_instance.workspace_release = self.workspace_release
        rel_instance.release = self.release
        rel_instance.save()
        return rel_instance


class PublishSerializer(serializers.Serializer):
    release = serializers.UUIDField(required=True)
    environments = serializers.ListField(required=True)
    host = serializers.UUIDField(required=True)

    def validate(self, data):
        try:
            release = Release.objects.get(pk=str(data["release"]))
            data["release"] = release
        except Release.DoesNotExist:
            raise serializers.ValidationError("This release does not exist")

        for index in range(len(data["environments"])):
            try:
                environment = EnvironmentRelease.objects.get(pk=data["environments"][index])
                data["environments"][index] = environment
            except EnvironmentRelease.DoesNotExist:
                raise serializers.ValidationError(
                    "The environment {0} does not exist".format(data["environments"][index])
                )

        try:
            host = Host.objects.get(pk=str(data["host"]))
            data["host"] = host
        except Host.DoesNotExist:
            raise serializers.ValidationError("This host does not exist")

        return data
