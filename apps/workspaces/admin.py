from django.contrib import admin

from apps.workspaces.forms import WorkspaceAdminForm
from apps.workspaces.models import Workspace, Environment, Integration, FunctionFile, Flow, Route, Release


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "creator", "team", "workspae_color_render"]
    list_display_links = ["name", "description", "creator", "team"]
    list_filter = ["creator", "team"]
    list_select_related = ("creator", "team")
    form = WorkspaceAdminForm


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)


@admin.register(FunctionFile)
class FunctionFileAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["path", "method", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team", "method"]
    search_fields = ["path", "description"]
    list_select_related = ("workspace",)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["published", "name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team", "published"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)
