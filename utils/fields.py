from apps.v1.core.widgets import JSONWidget
from django.contrib.postgres import fields as postgres_fields


class JSONField(postgres_fields.JSONField):
    widget = JSONWidget

    def clean(self, value):
        return {k: super().clean(v) for k, v in value.items()}
