from django.db import models
from django.utils.translation import gettext_lazy as _

from cers.core.models import CersModel


class Company(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        app_label = 'cers_auth'

    def __str__(self):
        return self.name