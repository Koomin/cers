import datetime

from django.conf import settings
from openpyxl import Workbook

from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _, get_language, activate, deactivate

from cers.companies.models import Company
from cers.tickets.models import TicketClosed


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--date_from')
        parser.add_argument('--date_to')
        parser.add_argument('--company_id')

    def handle(self, *args, **kwargs):
        report_name = _('Monthly report')
        queryset = TicketClosed.objects.filter(closed_date__gte=kwargs.get('date_from'),
                                               closed_date__lte=kwargs.get('date_to'),
                                               company__id=kwargs.get('company_id'))
        language_code = get_language()
        activate(language_code)
        headers = [_('No.'), _('Date'), _('Access to the client'), _('Description'), _('Duration of service')]
        wb = Workbook()
        ws = wb.active
        ws.append(str(obj) for obj in headers)
        for idx, obj in enumerate(queryset):
            ws.append([idx + 1,
                       obj.closed_date,
                       str(_('YES')) if obj.access_to_client else str(_('NO')),
                       obj.description,
                       obj.duration])
        file_name = f'{report_name}_' \
                    f'{Company.objects.get(id=kwargs.get("company_id")).name}_' \
                    f'{datetime.date.today()}.xlsx'
        path = f'{settings.MEDIA_ROOT}/reports/{file_name}'
        wb.save(path)
        deactivate()
        return file_name
