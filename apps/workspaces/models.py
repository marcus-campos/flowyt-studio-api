from django.contrib.postgres.fields import JSONField
from django.db import models


class Workspace(models.Model):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True, help_text="(Opcional)")
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")
    integrations = models.CharField("Integrações", max_length=255, null=True, blank=True, help_text="(Opcional)")
    envs = JSONField("Environments", null=True, blank=True, help_text="(Opcional)")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Flow(models.Model):
    name = models.CharField("Flow Name", max_length=255)
    flow_layout = JSONField("Flow Layout")
    flow_data = JSONField("Flow Data", null=True, blank=True, help_text="(Opcional)")

    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
