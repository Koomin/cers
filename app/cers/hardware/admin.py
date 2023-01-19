from cers.core.admin import CersModelAdmin, admin_site
from cers.hardware.models import Computer


class ComputerAdmin(CersModelAdmin):
    list_display = ['name', 'model', 'number', 'operating_system', 'office', 'bitlocker', 'backup', 'norton',
                    'synology_pass', 'comment', 'serial_number']


admin_site.register(Computer, ComputerAdmin)
