from django.urls import path


from . import views

urlpatterns = [
    path("", views.ListCreateTeamAPIView.as_view(), name="team"),
    path("build-sub-domain", views.SubDomainURLBuilderView.as_view(), name="sub-domain-build-url",),
    path(
        "<uuid:pk>/", views.RetrieveDestroyUpdateTeamAPIView.as_view(), name="retrieve-destroy-update-team",
    ),
    path("<uuid:pk>/invite/", views.InviteToTeamAPIView.as_view(), name="invite_to_team",),
    path("<uuid:pk>/remove/", views.RemoveFromTeamAPIView.as_view(), name="remove_member_from_team",),
]
