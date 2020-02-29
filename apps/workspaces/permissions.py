from rest_framework import permissions

from apps.teams.models import Team


class PermissionMixin:
    def get_workspace(self, obj):
        if hasattr(obj, "workspace"):
            workspace = obj.workspace
        elif hasattr(obj, "workspace_release"):
            workspace = obj.workspace_release
        else:
            workspace = obj
        return workspace


class IsCreatorPermission(permissions.IsAuthenticated, PermissionMixin):
    def has_object_permission(self, request, view, obj):
        workspace = self.get_workspace(obj)
        return request.user == workspace.creator


class IsInTeamPermission(IsCreatorPermission, PermissionMixin):
    def has_object_permission(self, request, view, obj):
        workspace = self.get_workspace(obj)
        if not workspace.id:
            return True
        allowed = super(IsInTeamPermission, self).has_object_permission(request, view, obj)
        user_profile = request.user.userprofile
        return allowed or Team.object.filter(id=workspace.team, members__in=[user_profile]).exists()
