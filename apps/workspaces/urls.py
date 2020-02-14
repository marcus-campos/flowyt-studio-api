from django.urls import include, path
from rest_framework import routers
from apps.workspaces import views

router = routers.DefaultRouter()
router.register(r"workspaces", views.WorkspaceViewSet)
router.register(r"flows", views.FlowViewSet)
router.register(r"environment", views.EnvironmentViewSet)
router.register(r"integration", views.IntegrationViewSet)
router.register(r"function-file", views.IntegrationViewSet)


urlpatterns = [
    path(
        "workspaces/<uuid:id>/release/", views.ReleaseView.as_view(), name="release"
    ),
    path("", include(router.urls)),
]
