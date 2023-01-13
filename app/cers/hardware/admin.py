from cers.core.admin import CersModelAdmin, admin_site
from cers.hardware.models import Computer


class ComputerAdmin(CersModelAdmin):
    list_display = ['name', 'model', 'mac_address', 'number', 'operating_system', 'office', 'bios_password',
                    'bitlocker', 'backup', 'ssd', 'norton', 'synology_pass', 'comment', 'vpn', 'serial_number']


admin_site.register(Computer, ComputerAdmin)
