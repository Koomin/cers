import datetime

from calendar import month_name

from django.contrib.admin import DateFieldListFilter, RelatedOnlyFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, deactivate
from django.db.models import Sum
from django.contrib import admin
from cers.core.duration_widget import TimeDurationWidget
from cers.core.admin import admin_site, CersModelAdmin
from cers.tickets.models import Comment, TicketOpen, TicketClosed, Attachment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


class TicketAdmin(CersModelAdmin):
    list_display = ['topic', 'deadline', 'status', 'accepted', 'priority', 'reporting', 'duration', 'company']
    inlines = (CommentInline, AttachmentInline)
    context_field = 'company'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if hasattr(self.form, 'cleaned_data') and self.form.cleaned_data.get('reporting'):
            obj.user = self.form.cleaned_data.get('reporting')
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.opts.object_name == 'Ticket':
            qs = qs.filter(status='open')
        return qs

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser:
            list_display = ['topic',
                            'deadline',
                            'status',
                            'accepted',
                            'priority',
                            'reporting',
                            'technician',
                            'duration',
                            'company',
                            'created',
                            ]
            self.list_editable = ['status',
                                  'priority',
                                  'technician',
                                  'duration',
                                  ]
        else:
            self.list_editable = []
        if (request.user.settings.get(
                'company') != 0 or request.user.companies.count() == 1) and 'company' in list_display:
            list_display.remove('company')
        return list_display

    def get_fields(self, request, obj=None):
        fields = ()
        if request.user.is_superuser:
            fields = (
                ('topic', 'technician'),
                ('description',),
                ('priority', 'status'),
                ('deadline',),
                ('duration',),
                ('access_to_client',),
            )
        elif request.user.is_manager and request.user.report_on_behalf:
            fields = (('reporting',), ('topic',), ('description',), ('priority',), ('deadline',),)
        elif request.user.is_manager:
            fields = (('topic',), ('description',), ('priority',), ('deadline',),)
        elif request.user.groups.name == 'user':
            fields = (('topic',), ('description',))
        elif request.user.groups.name == 'technician':
            fields = (
                ('topic',),
                ('description',),
                ('status',),
                ('access_to_client',),
                ('duration',),
            )

        return fields

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'duration':
            kwargs['widget'] = TimeDurationWidget(show_days=False, show_seconds=False)
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return formfield

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'technician':
            qs = super(TicketAdmin, self).get_field_queryset(db, db_field, request)
            return qs.filter(groups__name='technician')
        if db_field.name == 'reporting' and request.user.report_on_behalf:
            qs = super(TicketAdmin, self).get_field_queryset(db, db_field, request)
            return qs.filter(companies__in=request.user.companies.all())
        return super(TicketAdmin, self).get_field_queryset(db, db_field, request)

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser else False


@admin.register(TicketOpen)
class TicketOpenAdmin(TicketAdmin):
    change_form_template = 'tickets/change_form_open_ticket.html'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups and request.user.groups.name == 'user':
            qs = qs.filter(reporting=request.user)
        if request.user.groups and request.user.groups.name == 'technician':
            qs = qs.filter(technician=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            fields = ('topic', 'description')
        else:
            fields = ()
        return fields


class TicketClosedAdmin(TicketOpenAdmin):
    sum_fields = ['duration']

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        self.list_editable = []
        return list_display

    def changelist_view(self, request, extra_context=None):
        result = super().changelist_view(request, extra_context)
        try:
            qs = result.context_data['cl'].queryset
            today = datetime.datetime.now()
            month = today.month
            year = today.year
            qs = qs.filter(closed_date__year=year, closed_date__month=month)
            language_code = get_language()
            activate(language_code)
            month = str(_(month_name[month]))
            value = list(qs.aggregate(Sum('duration')).values())[0] or 0
            if value != 0:
                seconds = value.seconds
                hours = seconds // 3600
                minutes = (seconds // 60) % 60
                hours_name = _('hours')
                minutes_name = _('minutes')
                value = f"{hours} {hours_name} {minutes} {minutes_name}"
            sum_fields = [{'name': _('Period'),
                           'value': f'{month} {year}'
                           },
                          {
                              'name': _('For day'),
                              'value': datetime.date.today()
                          },
                          {
                              'name': _('Time'),
                              'value': value,
                          }]
            result.context_data['sum_fields'] = sum_fields
        except:  # noqa
            pass
        deactivate()
        return result

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True if request.user.is_superuser else False

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('technician', RelatedOnlyFieldListFilter), 'closed_date',


admin_site.register(TicketOpen, TicketOpenAdmin)
admin_site.register(TicketClosed, TicketClosedAdmin)
