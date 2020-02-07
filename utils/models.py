# -*- coding: UTF-8 -*-
import uuid

from django.db import models
from django.utils.translation import ugettext as translate
from django.utils.timezone import now


class AutoCreatedUpdatedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField("Criado em",null=True,blank=True,db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em",null=True, blank=True, db_index=True, auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):

    deleted_at = models.DateTimeField(
        verbose_name=translate('deleted at'),
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
            'using': using,
        }
        if hasattr(self, 'updated_at'):
            kwargs['disable_auto_updated_at'] = True
        self.save(**kwargs)


