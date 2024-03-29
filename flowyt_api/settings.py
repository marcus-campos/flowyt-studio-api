import os
from datetime import timedelta
from pathlib import Path

from django.utils.module_loading import import_string
from prettyconf import config

# Project Structure
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).absolute().parents[1]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="yyyyxxxxzzzz", cast=str)

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOGGERS = config("LOGGERS", default="", cast=config.list)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=config.list)


INSTALLED_APPS = [
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Rest Framework Apps
    "rest_framework",
    "drf_yasg",
    # Libs
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "cuser",
    "django_ace",
    # Apps
    "apps.workspaces",
    "apps.teams",
    "apps.accounts",
    "apps.hosts",
]
AUTH_USER_MODEL = "cuser.CUser"
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]


ROOT_URLCONF = "flowyt_api.urls"
WSGI_APPLICATION = "flowyt_api.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME", default="flowyt", cast=str),
        "USER": config("DATABASE_USER", default="postgres", cast=str),
        "PASSWORD": config("DATABASE_PASSWORD", default="postgres", cast=str),
        "HOST": config("DATABASE_HOST", default="127.0.0.1", cast=str),
        "PORT": config("DATABASE_PORT", default="5432", cast=str),
        "OPTIONS": {},
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (PROJECT_DIR / "locale",)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}},
    "JSON_EDITOR": True,
    "DEFAULT_API_URL": config("DEFAULT_API_URL", default=None),
}

# Accept all
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=7),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=10),
}

ENGINE_ENDPOINTS = {"publish": "/_engine/publish", "reload": "/_engine/reload", "setup": "/_engine/setup"}

EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = "Flowyt <noreply@flowyt.com>"

SITE_NAME = "Flowyt"
BASE_DOMAIN_URL = "flowyt.com"
BASE_PROTOCOL = "https://"

STUDIO_BASE_DOMAIN_URL = "{0}studio.{1}".format(BASE_PROTOCOL, BASE_DOMAIN_URL)

JET_SIDE_MENU_COMPACT = True

WORKSPACE_PUBLISH_MODE = config("WORKSPACE_PUBLISH_MODE", default="redis", cast=str)  # redis, upload
WORKSPACE_SUBDOMAIN_ENABLE = config("WORKSPACE_SUBDOMAIN_ENABLE", default=False, cast=bool)
WORKSPACE_PUBLISH_HOST = config("WORKSPACE_PUBLISH_HOST", default="", cast=str)

REDIS = {
    "WORKSPACES": {
        "HOST": config("REDIS_HOST", cast=str, default="127.0.0.1"),
        "PORT": config("REDIS_PORT", cast=int, default=6379),
        "PASSWORD": config("REDIS_PASSWORD", cast=str, default=""),
        "DB": 0,
    },
    "PLAN": {
        "HOST": config("REDIS_HOST", cast=str, default="127.0.0.1"),
        "PORT": config("REDIS_PORT", cast=int, default=6379),
        "PASSWORD": config("REDIS_PASSWORD", cast=str, default=""),
        "DB": 1,
    },
    "MONITOR": {
        "HOST": config("REDIS_HOST", cast=str, default="127.0.0.1"),
        "PORT": config("REDIS_PORT", cast=int, default=6379),
        "PASSWORD": config("REDIS_PASSWORD", cast=str, default=""),
        "DB": 2,
    },
}
