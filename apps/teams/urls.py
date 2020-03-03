from django.urls import path


from . import views

urlpatterns = [
    path("", views.CreateTeamAPIView.as_view(), name="team"),
    path("<uuid:pk>/", views.UpdateTeamAPIView.as_view(), name="update-team",),
    path("<uuid:pk>/invite/", views.InviteToTeamAPIView.as_view(), name="invite_to_team",),
]
