from django.contrib import admin

from cers.core.admin import CersModelAdmin, admin_site
from cers.imports.models import Import


class ImportAdmin(CersModelAdmin):
    list_display = ['type', 'created']


admin_site.register(Import, ImportAdmin)
