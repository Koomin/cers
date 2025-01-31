from cers.companies.models import Company
from cers.core.models import CersModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CersUser(AbstractUser, CersModel):
    groups = models.ForeignKey(
        Group, verbose_name=_('groups'), on_delete=models.SET_NULL, null=True, related_name='cers_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='cers_user',
        related_query_name='user',
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    companies = models.ManyToManyField(Company, verbose_name=_('Companies'))
    phone_number = models.CharField(max_length=9, null=True, blank=True, verbose_name=_('Phone number'))
    settings = models.JSONField(default={'company': 0}, null=True, blank=True, verbose_name=_('Settings'))
    report_on_behalf = models.BooleanField(default=False, verbose_name=_('Report on behalf'))
    color = models.CharField(max_length=255, default="", verbose_name=_('color'))

    @property
    def is_manager(self):
        if self.groups and self.groups.name == 'manager':
            return True
        return False

    def clean(self):
        super().clean()
        error_dict = {}
        if self._state.adding and self.username:
            try:
                CersUser.objects.get(username__iexact=self.username)
            except self.DoesNotExist:
                pass
            else:
                error_dict['username'] = ValidationError(_('User with given username already exist.'))
        if error_dict:
            raise ValidationError(error_dict)

    def save(self, *args, **kwargs):
        if self._state.adding:
            try:
                CersUser.objects.get(username__iexact=self.username)
            except self.DoesNotExist:
                pass
            else:
                raise ValidationError(_('User with given username already exist.'))
        if not self.settings.get('company'):
            self.settings['company'] = 0
        super().save(*args, **kwargs)
