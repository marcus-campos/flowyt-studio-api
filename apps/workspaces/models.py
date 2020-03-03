from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from django.template.defaultfilters import safe

from utils.models import AutoCreatedUpdatedMixin
from utils.choices import HTTPMethodChoices

User = get_user_model()


class Workspace(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    workspace_color = models.CharField("Workspace Color", null=True, blank=True, max_length=7)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "team"]

    def __str__(self):
        return self.name

    def workspae_color_render(self):
        html = """<div style='background-color:{0}; 
                    width:10px; height: 10px; 
                    display:inline-block; 
                    margin-right:5px;'></div>{0}""".format(
            self.workspace_color or "#FFFFFF"
        )
        return safe(html)

    workspae_color_render.short_description = "Workspace Color"


class Environment(AutoCreatedUpdatedMixin):
    name = models.CharField("Environment Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    environment_variables = JSONField("Environment variables", null=True, blank=True, help_text="(Opcional)")
    debug = models.BooleanField(default=False, help_text="(Default false)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["name", "workspace"]

    def __str__(self):
        return self.name


class Integration(AutoCreatedUpdatedMixin):
    name = models.CharField("Integration Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    integration_variables = JSONField("Environment variables", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["name", "workspace"]

    def __str__(self):
        return self.name


class FunctionFile(AutoCreatedUpdatedMixin):
    name = models.CharField("Function Name", max_length=255)
    function_data = models.TextField("Function data", null=True, blank=True, help_text="(Opcional)")
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["name", "workspace"]

    def __str__(self):
        return self.name


class Flow(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    flow_layout = JSONField("Flow Layout", null=True, blank=True, help_text="(Opcional)")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "workspace"]

    def __str__(self):
        return self.name


class Route(AutoCreatedUpdatedMixin):

    path = models.CharField("Path", max_length=255)
    method = models.CharField("HTTP Method", max_length=10, choices=HTTPMethodChoices.choices)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    active = models.BooleanField(default=True)

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)
    flow = models.ForeignKey("Flow", on_delete=models.CASCADE)

    class Meta:
        ordering = ["path"]
        unique_together = ["path", "method", "workspace"]

    def __str__(self):
        return self.path


class Release(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["updated_at"]
        unique_together = ["name", "workspace"]

    def __str__(self):
        return self.name


class WorkspaceRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    workspace_color = models.CharField("Workspace Name", null=True, blank=True, max_length=6)

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace = models.ForeignKey("Workspace", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FlowRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    flow_layout = JSONField("Flow Layout")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    flow = models.ForeignKey("Flow", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RouteRelease(AutoCreatedUpdatedMixin):
    path = models.CharField("Path", max_length=255)
    method = models.CharField("HTTP Method", max_length=10, choices=HTTPMethodChoices.choices)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    active = models.BooleanField(default=True)

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    flow_release = models.ForeignKey("FlowRelease", on_delete=models.CASCADE)
    route = models.ForeignKey("Route", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["path"]

    def __str__(self):
        return self.path


class EnvironmentRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Environment Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    environment_variables = JSONField("Environment variables", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    environment = models.ForeignKey("Environment", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class IntegrationRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Integration Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    integration_variables = JSONField("Environment variables", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    integration = models.ForeignKey("Integration", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class FunctionFileRelease(AutoCreatedUpdatedMixin):
    name = models.CharField("Function Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    function_data = models.TextField("Function data", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Release", on_delete=models.CASCADE)
    workspace_release = models.ForeignKey("WorkspaceRelease", on_delete=models.CASCADE)
    function_file = models.ForeignKey("FunctionFile", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name
