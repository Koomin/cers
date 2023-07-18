from cers.cers_auth.models import CersUser
from cers.companies.models import Company
from cers.core.models import CersModel
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    user = models.ForeignKey(CersUser, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('User'))
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Company'))

    class Meta:
        verbose_name = _('Computer')
        verbose_name_plural = _('Computers')


class ComponentModel(CersModel):
    model = models.CharField(max_length=255, verbose_name=_('Model'))
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name=_('Manufacturer'))
    driver_url = models.URLField(null=True, blank=True, verbose_name=_('Driver url'))

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.manufacturer.name} {self.model}'


class Component(CersModel):
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Serial number'))
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
    model = models.ForeignKey(GraphicCardModel, on_delete=models.CASCADE, verbose_name=_('Model'))

    class Meta:
        verbose_name = _('Graphic Card')
        verbose_name_plural = _('Graphic Cards')


class HardDrive(Component):
    model = models.ForeignKey(HardDriveModel, on_delete=models.CASCADE, verbose_name=_('Model'))

    class Meta:
        verbose_name = _('Hard Drive')
        verbose_name_plural = _('Hard Drive')


class Memory(Component):
    model = models.ForeignKey(MemoryModel, on_delete=models.CASCADE, verbose_name=_('Model'))

    class Meta:
        verbose_name = _('Memory')
        verbose_name_plural = _('Memories')


class ComputerModel(CersModel):
    name = models.CharField(max_length=70, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Computer model')
        verbose_name_plural = _('Computer models')

    def __str__(self):
        return self.name


class SerialNumberConfig(CersModel):
    computer_model = models.OneToOneField(ComputerModel, on_delete=models.CASCADE, verbose_name=_('Computer model'))
    prefix = models.CharField(max_length=20, default='', blank=True)
    suffix = models.CharField(max_length=20, default='', blank=True)
    number_length = models.PositiveIntegerField(default=5, verbose_name=_('Number length'))

    class Meta:
        verbose_name = _('Serial number config')
        verbose_name_plural = _('Serial number config')

    def __str__(self):
        return self.computer_model.name

    def get_next_number(self):
        if self.serial_number.last():
            next_number = self.serial_number.last().number + 1
        else:
            next_number = 1
        return next_number

    def generate_full_number(self):
        next_number = self.get_next_number()
        zeros_quantity = self.number_length - len(str(next_number))
        zeros = ''.join('0' for _ in range(0, zeros_quantity))
        full_number = f'{self.prefix}{zeros}{next_number}{self.suffix}'
        return full_number


class ComputerSet(CersModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Company'))
    model = models.ForeignKey(ComputerModel, null=True, on_delete=models.CASCADE, verbose_name=_('Model'))
    serial_number = models.CharField(max_length=255, verbose_name=_('Serial number'), null=True, blank=True)
    operating_system = models.ForeignKey(
        OperatingSystem, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Operating system')
    )
    operating_system_license_key = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Operating system license key')
    )
    processor = models.ForeignKey(ProcessorModel, on_delete=models.CASCADE, verbose_name=_('Processor'))
    processor_serial_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Processor serial number')
    )
    power_supply = models.ForeignKey(PowerSupplyModel, on_delete=models.CASCADE, verbose_name=_('Power supply'))
    power_supply_serial_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Power supply serial number')
    )
    motherboard = models.ForeignKey(MotherboardModel, on_delete=models.CASCADE, verbose_name=_('Motherboard'))
    motherboard_serial_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_('Motherboard serial number')
    )
    date_of_sale = models.DateField(verbose_name=_('Date of sale'))
    warranty = models.IntegerField(verbose_name=_('Warranty'))

    class Meta:
        verbose_name = _('Computer set')
        verbose_name_plural = _('Computer sets')

    def save(self, *args, **kwargs):
        if not self.serial_number:
            super().save(*args, **kwargs)
            self.serial_number = SerialNumber().generate_serial_number(self)
        super().save(*args, **kwargs)


class SerialNumber(CersModel):
    full_number = models.CharField(max_length=255, verbose_name=_('Full number'))
    number = models.PositiveIntegerField()
    computer_set = models.OneToOneField(ComputerSet, on_delete=models.CASCADE, null=True, blank=True)
    config = models.ForeignKey(
        SerialNumberConfig,
        on_delete=models.CASCADE,
        related_name='serial_number',
        verbose_name=_('Serial number config'),
    )

    class Meta:
        verbose_name = _('Serial number')
        verbose_name_plural = _('Serial numbers')

    def __str__(self):
        return self.full_number

    def generate_serial_number(self, computer_set):
        config = SerialNumberConfig.objects.get(computer_model=computer_set.model)
        self.config = config
        self.computer_set = computer_set
        self.full_number = config.generate_full_number()
        self.number = config.get_next_number()
        self.save()
        return self.full_number
