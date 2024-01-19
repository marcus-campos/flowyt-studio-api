from django.urls import include, path
from rest_framework import routers

from apps.workspaces import views

router = routers.DefaultRouter()
router.register(r"workspaces", views.WorkspaceViewSet)
router.register(r"flows", views.FlowViewSet)
router.register(r"environment", views.EnvironmentViewSet)
router.register(r"integration", views.IntegrationViewSet)
router.register(r"integration-list", views.IntegrationListViewSet)
router.register(r"function-file", views.FunctionFileViewSet)
router.register(r"releases", views.ReleaseViewSet)
router.register(r"routes", views.RouteViewSet)
router.register(r"languages", views.LanguageViewSet)
router.register(r"monitor", views.MonitorViewSet)


urlpatterns = [
    path("releases/workspaces/<uuid:id>/", views.ReleaseView.as_view(), name="release"),
    path(
        "releases/<uuid:id>/publish/",
        views.ReleasePublishView.as_view(),
        name="publish",
    ),
    path("", include(router.urls)),
]
