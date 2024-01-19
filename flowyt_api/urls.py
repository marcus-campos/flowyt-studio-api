from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from apps.accounts.views import TokenObtainPairWithUserInfoView

schema_view = get_schema_view(
    openapi.Info(
        title="Flowyt API",
        default_version="v1",
        description="API to save workspaces related items",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@flowyt.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "api/v1/token/",
        TokenObtainPairWithUserInfoView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    re_path(r"^api/v1/", include("apps.urls")),
    re_path(r"^jet/", include("jet.urls", "jet")),
    re_path(r"^admin/", admin.site.urls),
]
