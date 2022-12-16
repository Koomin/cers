from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CersAuthConfig(AppConfig):
    name = 'cers.cers_auth'
    verbose_name = _('Configuration')
    verbose_name_plural = _('Configuration')