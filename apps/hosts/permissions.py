from rest_framework import permissions


class IsInHostTeamMemberPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        allowed = super(IsInHostTeamMemberPermission, self).has_object_permission(request, view, obj)
        return allowed and request.user in obj.team.members.all()
