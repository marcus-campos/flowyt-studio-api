from django.contrib import admin

from .models import Team, TeamInvitation


class TeamInvitationInline(admin.TabularInline):
    model = TeamInvitation
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "description", "owner", "organization", "subdomain", "is_personal")
    search_fields = ["name", "description", "owner", "subdomain"]
    list_filter = ["is_personal"]
    inlines = [TeamInvitationInline]
