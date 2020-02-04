from django.db import models


class Workspace(models.Model):

    name = models.CharField("Workspace Name", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True, help_text="(Opcional)")
    slug = models.SlugField("Slug", null=True, blank=True, help_text="(Opcional)")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

