from django.db import models

from cers.core.models import CersModel


class Computer(CersModel):
    first_name = models.CharField()