from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.models import AutoCreatedUpdatedMixin


class Workspace(AutoCreatedUpdatedMixin):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")
    integrations = JSONField("Integrations", max_length=255, null=True, blank=True, help_text="(Opcional)")
    envs = JSONField("Environments", null=True, blank=True, help_text="(Opcional)")
    workspace_color = models.CharField("Workspace Name", null=True, blank=True, max_length=6)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Flow(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    flow_layout = JSONField("Flow Layout")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Releases(AutoCreatedUpdatedMixin):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)


    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return self.name

class WorkspaceReleases(AutoCreatedUpdatedMixin):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")

    release = models.ForeignKey("Releases", on_delete=models.CASCADE)


    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return self.name

class FlowReleases(AutoCreatedUpdatedMixin):
    name = models.CharField("Flow Name", max_length=255)
    flow_layout = JSONField("Flow Layout")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    workspace_release = models.ForeignKey("WorkspaceReleases", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name