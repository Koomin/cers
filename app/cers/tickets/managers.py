from django.db import models


class TicketClosedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='close')


class TicketOpenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='open')
