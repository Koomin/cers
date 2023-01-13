from cers.core.admin import CersModelAdmin, admin_site
from cers.hardware.models import Computer


class ComputerAdmin(CersModelAdmin):
    pass


admin_site.register(Computer, ComputerAdmin)
