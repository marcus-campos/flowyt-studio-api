from django.db import models


class HTTPMethodChoices(models.TextChoices):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    TRACE = "TRACE"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"


class MonitorDBChoices(models.TextChoices):
    MONGO = "MONGO"
