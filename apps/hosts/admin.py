from django.contrib import admin

from apps.hosts.models import Host


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ["host", "description", "team"]
    list_display_links = list_display
    list_filter = ["team"]
    search_fields = ["host", "description"]
