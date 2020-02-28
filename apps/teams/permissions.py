from rest_framework import permissions


class IsTeamOwnerPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        allowed = super(IsTeamOwnerPermission, self).has_object_permission(request, view, obj)
        return allowed and obj.owner == request.user
