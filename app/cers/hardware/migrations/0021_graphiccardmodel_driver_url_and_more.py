# Generated by Django 4.1.4 on 2023-03-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0020_computer_user_alter_serialnumber_computer_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphiccardmodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
        migrations.AddField(
            model_name='harddrivemodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
        migrations.AddField(
            model_name='memorymodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
        migrations.AddField(
            model_name='motherboardmodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
        migrations.AddField(
            model_name='powersupplymodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
        migrations.AddField(
            model_name='processormodel',
            name='driver_url',
            field=models.URLField(blank=True, null=True, verbose_name='Driver url'),
        ),
    ]
