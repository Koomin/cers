from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ImportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cers.imports'
    verbose_name = _('Imports')
