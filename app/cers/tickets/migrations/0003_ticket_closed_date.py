# Generated by Django 4.1.4 on 2023-01-10 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_access_to_client_alter_ticket_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='closed_date',
            field=models.DateField(blank=True, null=True, verbose_name='Closed date'),
        ),
    ]
