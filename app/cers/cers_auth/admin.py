from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from cers.cers_auth.models import CersUser
from cers.core.admin import admin_site


class CersUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number", "companies")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "report_on_behalf",
                    "groups",
                ),
            },
        ),
        (_("Settings"), {"fields": ("settings",)}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    filter_horizontal = (
        "user_permissions",
    )
    list_display = ['username', 'first_name', 'last_name', 'email', ]


admin_site.register(CersUser, CersUserAdmin)
admin_site.register(Group, GroupAdmin)
