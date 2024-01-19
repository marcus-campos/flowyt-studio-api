from django.urls import include, path

urlpatterns = [
    path("", include("apps.workspaces.urls")),
    path("teams/", include("apps.teams.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("hosts/", include("apps.hosts.urls")),
]
