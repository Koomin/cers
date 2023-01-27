from cers.core.admin import CersModelAdmin, admin_site
from cers.hardware.models import Computer, ComputerSet, Processor, HardDrive, Memory, PowerSupply, Motherboard, \
    OperatingSystem, Manufacturer


class ComputerAdmin(CersModelAdmin):
    list_display = ['name', 'model', 'number', 'operating_system', 'office', 'bitlocker', 'backup', 'norton',
                    'synology_pass', 'comment', 'serial_number']


class ComputerSetAdmin(CersModelAdmin):
    list_display = ['company', 'model', 'serial_number', 'operating_system', 'processor', 'hard_drive', 'memory_ram',
                    'power_supply', 'motherboard', 'date_of_sale', 'warranty']


class ComponentAdmin(CersModelAdmin):
    list_display = ['manufacturer', 'model']


admin_site.register(Computer, ComputerAdmin)
admin_site.register(ComputerSet, ComputerSetAdmin)
admin_site.register(Processor, ComponentAdmin)
admin_site.register(HardDrive, ComponentAdmin)
admin_site.register(Memory, ComponentAdmin)
admin_site.register(PowerSupply, ComponentAdmin)
admin_site.register(Motherboard, ComponentAdmin)
admin_site.register(OperatingSystem, CersModelAdmin)
admin_site.register(Manufacturer, CersModelAdmin)
