# Generated by Django 4.1.4 on 2023-01-30 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0015_computerset_operating_system_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computerset',
            name='operating_system_serial_number',
        ),
        migrations.AddField(
            model_name='computerset',
            name='operating_system_license_key',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Operating system license key'),
        ),
    ]
