from django.db import models
from django.utils.translation import gettext_lazy as _
from cers.companies.models import Company
from cers.core.models import CersModel


class Supplier(CersModel):
    name = models.CharField(max_length=120, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def __str__(self):
        return self.name


class Order(CersModel):
    class Status(models.TextChoices):
        proposed = 'proposed', _('Proposed')
        placed = 'placed', _('Placed')
        ordered = 'ordered', _('Ordered')
        on_site = 'on-site', _('On-site')
        for_release = 'for release', _('For release')
        delivered = 'delivered', _('Delivered')

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders', verbose_name=_('Company'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.CharField(max_length=120, choices=Status.choices, default=Status.placed, verbose_name=_('Status'))
    selling_price_gross = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Gross selling price'))
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            company = self.user.settings.get('company')
            if company != 0:
                self.company = Company.objects.get(pk=company)
            elif company == 0 or self.user.companies.count() == 1:
                self.company = self.user.companies.first()
        super().save(*args, **kwargs)


class Comment(CersModel):
    description = models.TextField(verbose_name=_('Description'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
