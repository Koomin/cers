from cers.core.admin import CersModelAdmin, admin_site
from cers.hardware.models import (
    Computer,
    ComputerModel,
    ComputerSet,
    GraphicCard,
    GraphicCardModel,
    HardDrive,
    HardDriveModel,
    Manufacturer,
    Memory,
    MemoryModel,
    MotherboardModel,
    OperatingSystem,
    PowerSupplyModel,
    ProcessorModel,
    SerialNumberConfig,
)
from django.contrib import admin


class ComputerAdmin(CersModelAdmin):
    list_display = [
        'name',
        'user',
        'company',
        'model',
        'number',
        'operating_system',
        'office',
        'bitlocker',
        'backup',
        'norton',
        'synology_pass',
        'comment',
        'serial_number',
    ]
    context_field = 'company'


class GraphicCardInline(admin.TabularInline):
    model = GraphicCard
    extra = 1


class MemoryInline(admin.TabularInline):
    model = Memory
    extra = 1


class HardDriveInline(admin.TabularInline):
    model = HardDrive
    extra = 1


class ComputerSetAdmin(CersModelAdmin):
    list_display = [
        'company',
        'model',
        'serial_number',
        'operating_system',
        'processor',
        'power_supply',
        'motherboard',
        'date_of_sale',
        'warranty',
    ]
    readonly_fields = ['serial_number']
    inlines = (HardDriveInline, MemoryInline, GraphicCardInline)


class ComponentAdmin(CersModelAdmin):
    list_display = ['manufacturer', 'model']


class SerialNumberConfigInline(admin.TabularInline):
    model = SerialNumberConfig


class ComputerModelAdmin(CersModelAdmin):
    list_display = ['name']
    inlines = [
        SerialNumberConfigInline,
    ]


admin_site.register(Computer, ComputerAdmin)
admin_site.register(ComputerSet, ComputerSetAdmin)
admin_site.register(ProcessorModel, ComponentAdmin)
admin_site.register(HardDriveModel, ComponentAdmin)
admin_site.register(GraphicCardModel, ComponentAdmin)
admin_site.register(MemoryModel, ComponentAdmin)
admin_site.register(PowerSupplyModel, ComponentAdmin)
admin_site.register(MotherboardModel, ComponentAdmin)
admin_site.register(OperatingSystem, CersModelAdmin)
admin_site.register(Manufacturer, CersModelAdmin)
admin_site.register(ComputerModel, ComputerModelAdmin)
