# Generated by Django 4.1.4 on 2022-12-20 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('topic', models.CharField(max_length=255, verbose_name='Topic')),
                ('description', models.TextField(verbose_name='Description')),
                ('deadline', models.DateField(verbose_name='Deadline')),
                ('status', models.CharField(choices=[('open', 'Open'), ('close', 'Closed')], default='open', max_length=5, verbose_name='Status')),
                ('send_notification', models.CharField(choices=[('sms', 'SMS'), ('email', 'E-mail'), ('no', "Don't notify")], default='no', max_length=5, verbose_name='Send notification')),
                ('priority', models.IntegerField(choices=[(4, 'Low'), (3, 'Normal'), (2, 'Important'), (1, 'Critical')], default=3, verbose_name='Priority')),
                ('duration', models.DurationField(blank=True, null=True, verbose_name='Duration')),
                ('accepted', models.BooleanField(default=False, verbose_name='Accepted')),
                ('reporting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Reporting')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Technician')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketClosed',
            fields=[
            ],
            options={
                'verbose_name': 'Closed ticket',
                'verbose_name_plural': 'Closed tickets',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='TicketOpen',
            fields=[
            ],
            options={
                'verbose_name': 'Open ticket',
                'verbose_name_plural': 'Open tickets',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tickets.ticket',),
        ),
    ]