# Generated by Django 4.1.4 on 2022-12-28 08:09

from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='technician')


class Migration(migrations.Migration):
    dependencies = [
        ('cers_auth', '0007_auto_20221220_2156'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
