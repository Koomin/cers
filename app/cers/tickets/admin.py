from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from durationwidget.widgets import TimeDurationWidget

from cers.core.admin import admin_site, CersModelAdmin
from cers.tickets.filters import AcceptedFilter
from cers.tickets.models import Comment, TicketOpen, TicketClosed, Attachment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


class TicketAdmin(CersModelAdmin):
    list_display = ['topic', 'deadline', 'status', 'accepted', 'priority', 'reporting', 'duration', 'company' ,'created']
    inlines = (CommentInline, AttachmentInline)
    context_field = 'company'

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
                            'created',
                            ]
            self.list_editable = ['status',
                                  'priority',
                                  'technician',
                                  'duration',
                                  ]
        else:
            self.list_editable = []
        if (request.user.settings.get('company') != 0 or request.user.companies.count() == 1) and 'company' in list_display:
            list_display.remove('company')
        return list_display

    def get_fields(self, request, obj=None):
        fields = ()
        if request.user.is_superuser:
            fields = (
                ('topic', 'technician'),
                ('description',),
                ('priority', 'status'),
                ('deadline', 'duration'),
            )
        elif request.user.is_manager:
            fields = (('topic',), ('description',), ('priority', 'deadline'),)
        elif request.user.groups.name == 'user':
            fields = (('topic',), ('description',))

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
        return super(TicketAdmin, self).get_field_queryset(db, db_field, request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin_site.register(TicketOpen, TicketOpenAdmin)
admin_site.register(TicketClosed, TicketClosedAdmin)
