from django.contrib import admin
from durationwidget.widgets import TimeDurationWidget

from cers.tickets.models import Ticket, Comment, TicketOpen, TicketClosed


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['topic', 'deadline', 'status', 'priority', 'reporting', 'created']
    inlines = (CommentInline,)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser:
            list_display = ['topic',
                            'deadline',
                            'status',
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

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'duration':
            kwargs['widget'] = TimeDurationWidget(show_days=False, show_seconds=False)
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        return formfield

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'technician':
            return super(TicketAdmin, self).get_field_queryset(db, db_field, request).filter(groups__name='technician')
        return super(TicketAdmin, self).get_field_queryset(db, db_field, request)


@admin.register(TicketOpen)
class TicketOpen(TicketAdmin):
    change_form_template = 'tickets/change_form_open_ticket.html'

    class Media:
        js = ('tickets/js/accept_tickets.js',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups and request.user.groups.name == 'user':
            qs = qs.filter(reporting=request.user)
        if request.user.is_superuser:
            qs = qs.filter(technician=request.user)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            fields = ('topic', 'description')
        else:
            fields = ()
        return fields


@admin.register(TicketClosed)
class TicketClosed(TicketOpen):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
