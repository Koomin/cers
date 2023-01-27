from django.db import models
from django.utils.translation import gettext_lazy as _
from cers.core.models import CersModel
from cers.companies.models import Company


class Manufacturer(CersModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


class OperatingSystem(CersModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Operating system')
        verbose_name_plural = _('Operating systems')


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


class ComponentModel(CersModel):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.manufacturer.name} {self.model}'


class Component(CersModel):
    serial_number = models.CharField(max_length=255, null=True, blank=True,
                                     verbose_name=_('Serial number'))
    computer_set = models.ForeignKey('ComputerSet', on_delete=models.CASCADE)


class ProcessorModel(ComponentModel):
    class Meta:
        verbose_name = _('Processor')
        verbose_name_plural = _('Processors')


class HardDriveModel(ComponentModel):
    class Meta:
        verbose_name = _('Hard Drive')
        verbose_name_plural = _('Hard Drive')


class MemoryModel(ComponentModel):
    class Meta:
        verbose_name = _('Memory')
        verbose_name_plural = _('Memory')


class GraphicCardModel(ComponentModel):
    class Meta:
        verbose_name = _('Graphic Card')
        verbose_name_plural = _('Graphic Cards')


class PowerSupplyModel(ComponentModel):
    class Meta:
        verbose_name = _('Power Supply')
        verbose_name_plural = _('Power Supplies')


class MotherboardModel(ComponentModel):
    class Meta:
        verbose_name = _('Motherboard')
        verbose_name_plural = _('Motherboards')


class GraphicCard(Component):
    model = models.ForeignKey(GraphicCardModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Graphic Card')
        verbose_name_plural = _('Graphic Cards')


class HardDrive(Component):
    model = models.ForeignKey(HardDriveModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Hard Drive')
        verbose_name_plural = _('Hard Drive')


class Memory(Component):
    model = models.ForeignKey(MemoryModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Memory')
        verbose_name_plural = _('Memories')


class ComputerSet(CersModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Company'))
    model = models.CharField(max_length=255, verbose_name=_('Model'))
    serial_number = models.CharField(max_length=255, verbose_name=_('Serial number'))
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name=_('Operating system'))
    processor = models.ForeignKey(ProcessorModel, on_delete=models.CASCADE, verbose_name=_('Processor'))
    processor_serial_number = models.CharField(max_length=255, null=True, blank=True,
                                               verbose_name=_('Processor serial number'))
    power_supply = models.ForeignKey(PowerSupplyModel, on_delete=models.CASCADE, verbose_name=_('Power supply'))
    power_supply_serial_number = models.CharField(max_length=255, null=True, blank=True,
                                                  verbose_name=_('Power supply serial number'))
    motherboard = models.ForeignKey(MotherboardModel, on_delete=models.CASCADE, verbose_name=_('Motherboard'))
    motherboard_serial_number = models.CharField(max_length=255, null=True, blank=True,
                                                 verbose_name=_('Motherboard serial number'))
    date_of_sale = models.DateField(verbose_name=_('Date of sale'))
    warranty = models.IntegerField(verbose_name=_('Warranty'))

    class Meta:
        verbose_name = _('Computer set')
        verbose_name_plural = _('Computer sets')
