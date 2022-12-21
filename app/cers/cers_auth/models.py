from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from cers.companies.models import Company
from cers.core.models import CersModel


class CersUser(AbstractUser, CersModel):
    groups = models.ForeignKey(Group,
                               verbose_name=_("groups"),
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='cers_user')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="cers_user",
        related_query_name="user",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_("Company"))
    phone_number = models.CharField(max_length=9, null=True, blank=True, verbose_name=_("Phone number"))
