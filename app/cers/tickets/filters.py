import calendar

from cers.tickets.models import TicketClosed
from django.contrib.admin import SimpleListFilter
from django.utils.translation import activate, get_language
from django.utils.translation import gettext_lazy as _


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


class MonthClosedFilter(SimpleListFilter):
    title = _('Month closed')
    parameter_name = 'closed_date__month'

    def lookups(self, request, model_admin):
        queryset = TicketClosed.objects.distinct('closed_date__month').values_list('closed_date__month', flat=True)
        language_code = get_language()
        activate(language_code)
        lookup = ((obj, _(calendar.month_name[obj])) for obj in queryset)
        return lookup

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset


class YearClosedFilter(SimpleListFilter):
    title = _('Year closed')
    parameter_name = 'closed_date__year'

    def lookups(self, request, model_admin):
        queryset = TicketClosed.objects.distinct('closed_date__year').values_list('closed_date__year', flat=True)
        lookup = ((obj, obj) for obj in queryset)
        return lookup

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset
