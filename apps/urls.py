from django.urls import path, include

urlpatterns = [
    path("", include("apps.workspaces.urls")),
    path("teams/", include("apps.teams.urls")),
    path("accounts/", include("apps.accounts.urls")),
]
