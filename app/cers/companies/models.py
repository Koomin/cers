from django.apps import apps

from cers.core.models import CersModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('name'))
    color = models.CharField(max_length=255, default="", verbose_name=_('color'), blank=True)
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        app_label = 'cers_auth'

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self._state.adding:
            self.color = "#000000"
            try:
                super().save(force_insert, force_update, using, update_fields)
                model = apps.get_model('cers_auth', 'CersUser')
                users = model.objects.filter(groups__name__in=["admin", "technician"])
                for user in users:
                    user.companies.add(self)
                    user.save()
            except Exception as e:
                pass
        super().save(force_insert, force_update, using, update_fields)

class Department(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('name'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        app_label = 'cers_auth'

    def __str__(self):
        return self.name


class CompanyConfig(CersModel):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, verbose_name=_('company'), related_name='config')
    logo = models.FileField(verbose_name=_('logo'))
    main_company = models.BooleanField(default=False, verbose_name=_('main company'))

    class Meta:
        verbose_name = _('Company config')
        verbose_name_plural = _('Company config')

    def clean(self):
        if self._meta.model.objects.filter(main_company=True).exists():
            msg = _('Cannot add another main company.')
            raise ValidationError({'main_company': ValidationError(msg)})
        super().clean()
