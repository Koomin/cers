from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompaniesConfig(AppConfig):
    name = 'cers.companies'
    verbose_name = _('Company')
    verbose_name_plural = _('Companies')
