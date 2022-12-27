from django.db import models
from django.utils.translation import gettext_lazy as _

from cers.cers_auth.models import CersUser
from cers.core.models import CersModel
from cers.tickets.managers import TicketOpenManager, TicketClosedManager


class Ticket(CersModel):
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        CLOSED = 'close', _('Closed')

    class NotificationType(models.TextChoices):
        SMS = 'sms', _('SMS')
        EMAIL = 'email', _('E-mail')
        NO = 'no', _('Don\'t notify')

    class PriorityLevels(models.IntegerChoices):
        LOW = 4, _('Low')
        NORMAL = 3, _('Normal')
        IMPORTANT = 2, _('Important')
        CRITICAL = 1, _('Critical')

    reporting = models.ForeignKey(CersUser, on_delete=models.CASCADE, null=False, blank=True,
                                  verbose_name=_('Reporting'), related_name='reporting_tasks')
    technician = models.ForeignKey(CersUser, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks',
                                   verbose_name=_('Technician'))
    topic = models.CharField(max_length=255, null=False, blank=False, verbose_name=_('Topic'))
    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))
    deadline = models.DateField(null=True, blank=True, verbose_name=_('Deadline'))
    status = models.CharField(max_length=5, choices=Status.choices, blank=False, null=False, default=Status.OPEN,
                              verbose_name=_('Status'))
    send_notification = models.CharField(max_length=5, choices=NotificationType.choices, blank=False, null=False,
                                         default=NotificationType.NO, verbose_name=_('Send notification'))
    priority = models.IntegerField(choices=PriorityLevels.choices, blank=False, null=False,
                                   default=PriorityLevels.NORMAL, verbose_name=_('Priority'))
    duration = models.DurationField(null=True, blank=True, verbose_name=_('Duration'))
    accepted = models.BooleanField(default=False, verbose_name=_('Accepted'))

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        # TODO Changing status require duration filled
        if self._state.adding:
            self.reporting = self.user
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)


class TicketOpen(Ticket):
    objects = TicketOpenManager()

    class Meta:
        proxy = True
        verbose_name = _('Open ticket')
        verbose_name_plural = _('Open tickets')


class TicketClosed(Ticket):
    objects = TicketClosedManager()

    class Meta:
        proxy = True
        verbose_name = _('Closed ticket')
        verbose_name_plural = _('Closed tickets')


class TicketOpenAdmin(Ticket):
    objects = TicketOpenManager()

    class Meta:
        proxy = True
        verbose_name = _('Open ticket +')
        verbose_name_plural = _('Open tickets +')


class TicketClosedAdmin(Ticket):
    objects = TicketClosedManager()

    class Meta:
        proxy = True
        verbose_name = _('Closed ticket +')
        verbose_name_plural = _('Closed tickets +')


class Comment(CersModel):
    description = models.TextField(verbose_name=_('Description'))
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
