from cers.cers_auth.actions import add_companies
from cers.cers_auth.models import CersUser
from cers.core.admin import admin_site
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class CersUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'companies')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'report_on_behalf',
                    'groups',
                ),
            },
        ),
        (_('Settings'), {'fields': ('settings', 'color')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('user_permissions',)
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    actions = (add_companies,)


admin_site.register(CersUser, CersUserAdmin)
admin_site.register(Group, GroupAdmin)
