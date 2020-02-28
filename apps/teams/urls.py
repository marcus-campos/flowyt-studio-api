from django.urls import path


from . import views

urlpatterns = [
    path(r"^$", views.CreateTeamAPIView.as_view(), name="team"),
    path(r"^(?P<pk>[\w\-]+)/$", views.UpdateTeamAPIView.as_view(), name="update-team",),
    path(r"^(?P<pk>[\w\-]+)/invite/$", views.InviteToTeamAPIView.as_view(), name="invite_to_team",),
]
