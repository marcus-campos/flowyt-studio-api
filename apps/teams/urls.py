from django.conf.urls import url


from . import views

urlpatterns = [
    url(r"^$", views.CreateTeamAPIView.as_view(), name="team"),
    url(r"^(?P<pk>[\w\-]+)/$", views.UpdateTeamAPIView.as_view(), name="update-team",),
    url(r"^(?P<pk>[\w\-]+)/invite/$", views.InviteToTeamAPIView.as_view(), name="invite_to_team",),
]
