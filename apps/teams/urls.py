from django.urls import path


from . import views

urlpatterns = [
    path("", views.ListCreateTeamAPIView.as_view(), name="team"),
    path("<uuid:pk>/", views.RetriveDestroyUpdateTeamAPIView.as_view(), name="retrive-destroy-update-team",),
    path("<uuid:pk>/invite/", views.InviteToTeamAPIView.as_view(), name="invite_to_team",),
]
