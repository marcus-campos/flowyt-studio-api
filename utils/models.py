# -*- coding: UTF-8 -*-
import uuid
from itertools import chain

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as translate


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


class AutoCreatedUpdatedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("Criado em", null=True, blank=True, db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", null=True, blank=True, db_index=True, auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(
        verbose_name=translate("deleted at"),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        kwargs = {
            "using": using,
        }
        if hasattr(self, "updated_at"):
            kwargs["disable_auto_updated_at"] = True
        self.save(**kwargs)
