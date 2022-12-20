from django.contrib import admin

from cers.tickets.models import Ticket, Comment, TicketOpen, TicketOpenAdmin, TicketClosedAdmin, TicketClosed


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('topic', 'deadline', 'status', 'priority', 'reporting', 'created')
    inlines = (CommentInline,)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.is_superuser:
            list_display = ('topic',
                            'deadline',
                            'status',
                            'priority',
                            'reporting',
                            'technician',
                            'duration',
                            'created',
                            )
            self.list_editable = ('status',
                                  'priority',
                                  'reporting',
                                  'technician',
                                  'duration',)
        return list_display

    def get_fields(self, request, obj=None):
        fields = ()
        if request.user.is_superuser:
            fields = (
                ('topic', 'technician'),
                ('description',),
                ('priority', 'status'),
                ('deadline', 'send_notification'),
                ('duration',)
            )
        elif request.user.groups.name == 'manager':
            fields = (('topic',), ('description',), ('priority', 'deadline'),)
        elif request.user.groups.name == 'user':
            fields = (('topic',), ('description',))

        return fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(TicketOpen)
class TicketOpen(TicketAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.name == 'user':
            qs = qs.filter(reporting=request.user)
        return qs

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            fields = ('topic', 'description')
        else:
            fields = ()
        return fields


@admin.register(TicketClosed)
class TicketClosed(TicketOpen):
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TicketOpenAdmin)
class TicketOpenSuperAdmin(TicketAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            qs = qs.filter(accepted=True)
        return qs


@admin.register(TicketClosedAdmin)
class TicketClosedSuperAdmin(TicketAdmin):
    def has_change_permission(self, request, obj=None):
        return False
