import uuid as uuid_lib
from django.db import models
from django.utils.translation import gettext_lazy as _


class CersModel(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))

    class Meta:
        abstract = True
