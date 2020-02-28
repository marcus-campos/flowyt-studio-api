from django.db import models
from utils.models import AutoCreatedUpdatedMixin


class Host(AutoCreatedUpdatedMixin):
    host = models.CharField("Host", max_length=255)
    secret_token = models.CharField("Secret", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name
