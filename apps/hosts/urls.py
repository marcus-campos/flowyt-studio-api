from django.urls import include, path
from rest_framework import routers
from apps.hosts import views

urlpatterns = [
    path("", views.HostViewSet.as_view()),
    path("<uuid:pk>/", views.HostDetailViewSet.as_view()),
]
