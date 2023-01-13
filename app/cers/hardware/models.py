from django.db import models
from django.utils.translation import gettext_lazy as _
from cers.core.models import CersModel


class Computer(CersModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Name'))
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Model'))
    mac_address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('MAC address'))
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Computer number'))
    operating_system = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Operating system'))
    office = models.CharField(max_length=120, null=True, blank=True, verbose_name=_('Office'))
    bios_password = models.CharField(max_length=120, null=True, blank=True, verbose_name=_('Bios password'))
    bitlocker = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Bitlocker'))
    backup = models.BooleanField(default=False, verbose_name=_('Backup'))
    ssd = models.BooleanField(default=False, verbose_name=_('SSD'))
    norton = models.CharField(max_length=70, null=True, blank=True, verbose_name=_('Norton'))
    synology_pass = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Synology password'))
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Comment'))
    vpn = models.BooleanField(default=False, verbose_name=_('VPN'))
    serial_number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Serial number'))

    class Meta:
        verbose_name = _('Computer')
        verbose_name_plural = _('Computers')
