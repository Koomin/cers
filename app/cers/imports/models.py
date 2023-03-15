from cers.core.models import CersModel
from django.core.management import call_command
from django.db import models
from django.utils.translation import gettext_lazy as _


class Import(CersModel):
    class Type(models.TextChoices):
        COMPUTER = 'import_computers', _('Import computers')

    file = models.FileField(upload_to='imports/', blank=False, null=False, verbose_name=_('File'))
    type = models.CharField(max_length=255, choices=Type.choices, blank=False, null=False, verbose_name=_('Type'))

    class Meta:
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        call_command(self.type, file=self.file.path)
