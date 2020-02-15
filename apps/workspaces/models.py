from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.models import AutoCreatedUpdatedMixin


class Workspace(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")
    workspace_color = models.CharField(
        "Workspace Name", null=True, blank=True, max_length=6
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Environment(AutoCreatedUpdatedMixin):
    name = models.CharField("Environment Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    environment_variables = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )
    debug = models.BooleanField(default=False, help_text="(Default false)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class Integration(AutoCreatedUpdatedMixin):
    name = models.CharField("Integration Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    integration_variables = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class FunctionFile(AutoCreatedUpdatedMixin):
    name = models.CharField("Function Name", max_length=255)
    function_data = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class Flow(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    flow_layout = JSONField(
        "Flow Layout", null=True, blank=True, help_text="(Opcional)"
    )
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Release(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return self.name


class WorkspaceRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")
    workspace_color = models.CharField(
        "Workspace Name", null=True, blank=True, max_length=6
    )

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FlowRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    flow_layout = JSONField("Flow Layout")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    flow = models.ForeignKey("Flow", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class EnvironmentRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Environment Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    environment_variables = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    environment = models.ForeignKey("Environment", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class IntegrationRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Integration Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    integration_variables = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    integration = models.ForeignKey("Integration", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class FunctionFileRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Function Name", max_length=255)
    description = models.TextField(
        "Description", null=True, blank=True, help_text="(Opcional)"
    )
    function_data = JSONField(
        "Environment variables", null=True, blank=True, help_text="(Opcional)"
    )

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    function_file = models.ForeignKey("FunctionFile", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name
