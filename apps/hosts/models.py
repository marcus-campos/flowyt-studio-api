from django.db import models
from utils.models import AutoCreatedUpdatedMixin


class Host(AutoCreatedUpdatedMixin):
    host = models.CharField("Host", max_length=255)
    secret_token = models.CharField("Secret", max_length=255)
    description = models.TextField("Description", null=True, blank=True, help_text="(Opcional)")
    team = models.ForeignKey(
        "teams.Team", on_delete=models.CASCADE, null=True, blank=True, related_name="team_hosts"
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.host
