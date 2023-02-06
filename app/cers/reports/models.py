from django.db import models
from django.utils.translation import gettext_lazy as _

from cers.companies.models import Company
from cers.core.models import CersModel


class ReportGeneration(CersModel):
    class ReportType(models.TextChoices):
        MONTHLY_REPORT = 'monthly_report', _('Monthly report')

    report_type = models.CharField(max_length=50, choices=ReportType.choices, blank=False, null=False,
                                   verbose_name=_('Report type'))
    date_from = models.DateField(null=False, blank=False, verbose_name=_('Date from'))
    date_to = models.DateField(null=False, blank=False, verbose_name=_('Date to'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Company'))

    class Meta:
        verbose_name = _('Reports generation')
        verbose_name_plural = _('Reports generation')

    def __str__(self):
        return f'{self.report_type} {self.date_from} - {self.date_to}'
