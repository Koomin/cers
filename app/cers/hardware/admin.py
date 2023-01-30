from cers.core.admin import CersModelAdmin, admin_site
from django.contrib import admin
from cers.hardware.models import Computer, ComputerSet, HardDrive, Memory, OperatingSystem, Manufacturer, GraphicCard, \
    ProcessorModel, HardDriveModel, MemoryModel, PowerSupplyModel, MotherboardModel


class ComputerAdmin(CersModelAdmin):
    list_display = ['name', 'model', 'number', 'operating_system', 'office', 'bitlocker', 'backup', 'norton',
                    'synology_pass', 'comment', 'serial_number']


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
    list_display = ['company', 'model', 'serial_number', 'operating_system', 'processor', 'power_supply', 'motherboard',
                    'date_of_sale', 'warranty']
    inlines = (HardDriveInline, MemoryInline, GraphicCardInline)


class ComponentAdmin(CersModelAdmin):
    list_display = ['manufacturer', 'model']


admin_site.register(Computer, ComputerAdmin)
admin_site.register(ComputerSet, ComputerSetAdmin)
admin_site.register(ProcessorModel, ComponentAdmin)
admin_site.register(HardDriveModel, ComponentAdmin)
admin_site.register(GraphicCard, ComponentAdmin)
admin_site.register(MemoryModel, ComponentAdmin)
admin_site.register(PowerSupplyModel, ComponentAdmin)
admin_site.register(MotherboardModel, ComponentAdmin)
admin_site.register(OperatingSystem, CersModelAdmin)
admin_site.register(Manufacturer, CersModelAdmin)
