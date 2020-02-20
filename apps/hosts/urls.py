from django.urls import include, path
from rest_framework import routers
from apps.hosts import views

router = routers.DefaultRouter()
router.register(r"details", views.HostDetailViewSet)
router.register(r"", views.HostViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
