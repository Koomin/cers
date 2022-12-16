from django.db import models

from cers.core.models import CersModel


class Company(CersModel):
    name = models.CharField(max_length=255, null=False, blank=False)
