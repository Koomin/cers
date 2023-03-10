# Generated by Django 4.1.4 on 2023-01-19 17:23

from django.db import migrations, models


def change_norton(apps, schema_editor):
    Computer = apps.get_model('hardware', 'Computer')
    Computer.objects.filter(norton__isnull=False).update(norton_installed=True)


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0005_alter_computer_bios_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computer',
            name='bios_password',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='mac_address',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='ssd',
        ),
        migrations.AddField(
            model_name='computer',
            name='norton_installed',
            field=models.BooleanField(default=False, verbose_name='Norton'),
        ),
        migrations.RunPython(change_norton)
    ]
