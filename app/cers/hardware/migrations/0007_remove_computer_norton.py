# Generated by Django 4.1.4 on 2023-01-19 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0006_remove_computer_bios_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='computer',
            name='norton',
        ),
    ]
