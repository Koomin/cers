from django.db import models
from django.utils.translation import gettext_lazy as _
from cers.core.models import CersModel
from companies.models import Company


class OperatingSystem(CersModel):
    name = models.CharField(max_length=255)


class Computer(CersModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Name'))
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Model'))
    number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Computer number'))
    operating_system = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Operating system'))
    office = models.CharField(max_length=120, null=True, blank=True, verbose_name=_('Office'))
    bitlocker = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Bitlocker'))
    backup = models.BooleanField(default=False, verbose_name=_('Backup'))
    norton = models.BooleanField(default=False, verbose_name=_('Norton'))
    synology_pass = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Synology password'))
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Comment'))
    serial_number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Serial number'))

    class Meta:
        verbose_name = _('Computer')
        verbose_name_plural = _('Computers')


class Processor(CersModel):
    pass


class HardDrive(CersModel):
    pass


class Memory(CersModel):
    pass


class PowerSupply(CersModel):
    pass


class Motherboard(CersModel):
    pass


class ComputerSet(CersModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE, null=True, blank=True)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    processor_serial_number = models.CharField(max_length=255, null=True, blank=True)
    hard_drive = models.ForeignKey(HardDrive, on_delete=models.CASCADE)
    hard_drive_serial_number = models.CharField(max_length=255, null=True, blank=True)
    memory_ram = models.ForeignKey(Memory, on_delete=models.CASCADE)
    memory_ram_serial_number = models.CharField(max_length=255, null=True, blank=True)
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE)
    power_supply_serial_number = models.CharField(max_length=255, null=True, blank=True)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    motherboard_serial_number = models.CharField(max_length=255, null=True, blank=True)
    date_of_sale = models.DateField()
    warranty = models.IntegerField()
