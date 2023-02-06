from django.core.management import call_command
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('Company'))
    report_file = models.FileField(upload_to='reports/', blank=True, null=True, verbose_name=_('Report file'))

    class Meta:
        verbose_name = _('Reports generation')
        verbose_name_plural = _('Reports generation')

    def __str__(self):
        return f'{self.ReportType(self.report_type).label} {self.date_from} - {self.date_to}'

    def get_options(self):
        fields = ('date_from', 'date_to', 'company_id')
        options = {}
        for field in fields:
            val = getattr(self, field)
            if val:
                options[field] = val
        return options

    def save(self, *args, **kwargs):
        if self._state.adding:
            file = call_command(self.report_type, **self.get_options())
            self.report_file = file
        super().save(*args, **kwargs)
