from django.urls import path


from . import views

urlpatterns = [
    path(r"^create/$", views.CreateTeamAPIView.as_view(), name="login"),
    path(
        r"^(?P<pk>[\w\-]+)/invite/$",
        views.InviteToTeamAPIView.as_view(),
        name="invite_to_team",
    ),
]
