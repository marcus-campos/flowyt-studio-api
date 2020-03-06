from django.contrib import admin
from jet.admin import CompactInline

from apps.workspaces.forms import WorkspaceAdminForm
from apps.workspaces.models import (
    Workspace,
    Environment,
    Integration,
    FunctionFile,
    Flow,
    Route,
    Release,
    WorkspaceRelease,
    FlowRelease,
    RouteRelease,
    FunctionFileRelease,
    IntegrationRelease,
    EnvironmentRelease,
)


class ReleaseInline(CompactInline):
    model = Release
    extra = 0


class FlowInline(CompactInline):
    model = Flow
    extra = 0


class RouteInline(CompactInline):
    model = Route
    extra = 0


class EnvironmentInline(CompactInline):
    model = Environment
    extra = 0


class IntegrationInline(CompactInline):
    model = Integration
    extra = 0


class FunctionFileInline(CompactInline):
    model = FunctionFile
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "creator", "team", "workspae_color_render"]
    list_display_links = ["name", "description", "creator", "team"]
    list_filter = ["creator", "team"]
    list_select_related = ("creator", "team")
    form = WorkspaceAdminForm
    inlines = [
        ReleaseInline,
        FlowInline,
        RouteInline,
        EnvironmentInline,
        IntegrationInline,
        FunctionFileInline,
    ]

    def save_model(self, request, obj, form, change):
        result = super(WorkspaceAdmin, self).save_model(request, obj, form, change)
        if not change:
            debug_env = Environment()
            debug_env.name = "debug"
            debug_env.description = "Debug Environment"
            debug_env.workspace = obj
            debug_env.can_delete = False
            debug_env.debug = True
            debug_env.save()
        return result


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.can_delete
        return True


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


class WorkspaceReleaseInline(CompactInline):
    model = WorkspaceRelease
    extra = 0


class FlowReleaseInline(CompactInline):
    model = FlowRelease
    extra = 0


class RouteReleaseInline(CompactInline):
    model = RouteRelease
    extra = 0


class EnvironmentReleaseInline(CompactInline):
    model = EnvironmentRelease
    extra = 0


class IntegrationReleaseInline(CompactInline):
    model = IntegrationRelease
    extra = 0


class FunctionFileReleaseInline(CompactInline):
    model = FunctionFileRelease
    extra = 0


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["published", "name", "description", "workspace"]
    list_display_links = list_display
    list_filter = ["workspace", "workspace__team", "published"]
    search_fields = ["name", "description"]
    list_select_related = ("workspace",)

    inlines = [
        WorkspaceReleaseInline,
        FlowReleaseInline,
        RouteReleaseInline,
        EnvironmentReleaseInline,
        IntegrationReleaseInline,
        FunctionFileReleaseInline,
    ]
