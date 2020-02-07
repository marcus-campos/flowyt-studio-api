from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.models import AutoCreatedUpdatedMixin


class Workspace(AutoCreatedUpdatedMixin):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True, help_text="(Opcional)")
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")
    integrations = JSONField("Integrações", max_length=255, null=True, blank=True, help_text="(Opcional)")
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

    def __str__(self):
        return self.name
