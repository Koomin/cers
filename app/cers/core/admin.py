from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache

from cers.tickets.models import TicketOpen, TicketClosed


class CersAdmin(AdminSite):
    site_header = 'CERS'
    index_template = 'index.html'

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return app_list

    def index(self, request, extra_context=None):
        opened_tickets = TicketOpen.objects.all()
        closed_tickets = TicketClosed.objects.all()
        if request.user.is_superuser or request.user.is_manager:
            # opened_tickets = opened_tickets.count()
            # closed_tickets = closed_tickets.count()
            kwargs = {'company': None}
            if request.user.settings.get('company') and request.user.settings.get('company') != 0:
                kwargs = {'company__pk': request.user.settings.get('company')}
            elif request.user.settings.get('company') and request.user.settings.get('company') == 0:
                kwargs = {'company__pk__in': request.user.companies.values_list('pk', flat=True)}
            opened_tickets = opened_tickets.filter(**kwargs).count()
            closed_tickets = closed_tickets.filter(**kwargs).count()
        elif request.user.groups and request.user.groups.name == 'user':
            opened_tickets = opened_tickets.filter(reporting=request.user).count()
            closed_tickets = closed_tickets.filter(reporting=request.user).count()
        elif request.user.groups and request.user.groups.name == 'technician':
            opened_tickets = opened_tickets.filter(technician=request.user).count()
            closed_tickets = closed_tickets.filter(technician=request.user).count()
        else:
            opened_tickets = 0
            closed_tickets = 0
        context = {**self.each_context(request),
                   'title': _('Dashboard'),
                   'open_tasks_count': opened_tickets,
                   'closed_tasks_count': closed_tickets,
                   **(extra_context or {}), }
        return TemplateResponse(request, 'index.html', context)

    @property
    def urls(self):
        return self.get_urls(), "admin", self.name


admin_site = CersAdmin(name='cers_admin')


class CersModelAdmin(admin.ModelAdmin):
    context_field = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        filter_kwargs = None
        if self.context_field and request.user.settings.get('company') != 0:
            filter_kwargs = {f'{self.context_field}__pk': request.user.settings.get('company')}
        elif self.context_field and request.user.settings.get('company') == 0:
            filter_kwargs = {f'{self.context_field}__pk': request.user.companies.values_list('pk', flat=True)}
        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)
        return qs

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)