from django.urls import include, path
from rest_framework import routers
from apps.workspaces import views

router = routers.DefaultRouter()
router.register(r'/workspaces', views.WorkspaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]