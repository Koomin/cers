from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HardwareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cers.hardware'
    verbose_name = _('Hardware')