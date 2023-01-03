from django.utils.translation import gettext_lazy as _

from django.contrib.admin import SimpleListFilter


class AcceptedFilter(SimpleListFilter):
    title = _('Accepted')
    parameter_name = 'accepted'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(accepted=True)
        if self.value() == 'no':
            return queryset.filter(accepted=False)
