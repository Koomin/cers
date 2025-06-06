import datetime

from cers.companies.models import Company
from cers.reports.utils import Colors, color_font_row, color_row, set_borders
from cers.tickets.models import TicketClosed
from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Sum
from django.utils.translation import activate, deactivate, get_language
from django.utils.translation import gettext_lazy as _
from openpyxl import Workbook


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--date_from')
        parser.add_argument('--date_to')
        parser.add_argument('--company_id')

    def handle(self, *args, **kwargs):
        report_name = _('Monthly report by deadline')
        wb = Workbook()
        companies = [kwargs.get('company_id')] if kwargs.get('company_id') else list(
            Company.objects.all().values_list('id', flat=True))
        for company in companies:
            queryset = TicketClosed.objects.filter(
                deadline__gte=kwargs.get('date_from'),
                deadline__lte=kwargs.get('date_to'),
                company__id=company,
            ).order_by('deadline')
            language_code = get_language()
            activate(language_code)
            headers = [
                _('No.'),
                _('Deadline'),
                _('Access to the client'),
                _('Description'),
                _('Duration of service'),
                _('Reporting'),
            ]
            ws = wb.create_sheet(title=Company.objects.get(pk=company).name)
            ws.append(str(obj) for obj in headers)
            access_to_client = 0
            for idx, obj in enumerate(queryset, 1):
                if obj.access_to_client:
                    access_to_client += 1
                ws.append(
                    [
                        idx,
                        obj.deadline,
                        str(_('YES')) if obj.access_to_client else str(_('NO')),
                        obj.description,
                        obj.duration,
                        obj.reporting.username,
                    ]
                )
                if idx % 2 == 0 or queryset.count() == idx:
                    color_row(ws, idx if idx != queryset.count() else idx + 1,
                              Colors.GREY)
            color_row(ws, 1, Colors.BLACK)
            color_font_row(ws, 1, Colors.WHITE)
            ws.append(['', '', access_to_client, '',
                       queryset.aggregate(sum_duration=Sum('duration'))[
                           'sum_duration']])
            set_borders(ws, queryset.count() + 2)
            filters = ws.auto_filter
            filters.ref = f'A1:F{queryset.count()}'
            ws.column_dimensions['E'].width = 18
            ws.column_dimensions['B'].width = 12
            ws.column_dimensions['D'].width = 55
            ws.column_dimensions['C'].width = 8
            ws.column_dimensions['F'].width = 18
            ws.column_dimensions['G'].width = 18
        file_name = (
            f'{report_name}_'
            f'{Company.objects.get(id=kwargs.get("company_id")).name if kwargs.get("company_id") else "All companies"}_'
            f'{datetime.date.today()}.xlsx'
        )
        path = f'{settings.MEDIA_ROOT}/reports/{file_name}'
        wb.save(path)
        deactivate()
        return file_name
