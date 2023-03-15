from cers.core.models import CersModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('name'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        app_label = 'cers_auth'

    def __str__(self):
        return self.name


class Department(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('name'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        app_label = 'cers_auth'

    def __str__(self):
        return self.name
