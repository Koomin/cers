# Generated by Django 4.1.4 on 2023-03-01 16:15
import random
import string

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q


def password_generator():
    letters = string.ascii_lowercase
    password = ''.join(random.choice(letters) for i in range(12))
    return password


def name_extractor(name):
    name = name.split(' ')
    try:
        first_name = name[0]
    except IndexError:
        first_name = None
    try:
        last_name = name[1]
    except IndexError:
        last_name = None
    return first_name, last_name


def username_generator(name):
    first_name, last_name = name_extractor(name)
    if first_name and last_name:
        return f'{first_name[0]}.{last_name.title()}'
    elif first_name:
        return first_name
    else:
        return last_name


def update_user(apps, schema_editor):
    CersUser = apps.get_model('cers_auth', 'CersUser')
    Computer = apps.get_model('hardware', 'Computer')
    for obj in Computer.objects.filter(name__icontains=' ').exclude(name__icontains='tablet').exclude(name__icontains='novodworski'):
        new_user, created = CersUser.objects.get_or_create(username=username_generator(obj.name),
                                                           defaults={
                                                               'password': password_generator(),
                                                               'first_name': name_extractor(obj.name)[0],
                                                               'last_name': name_extractor(obj.name)[1],
                                                               'is_staff': False
                                                           }
                                                           )
        obj.user = new_user
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0019_alter_serialnumberconfig_prefix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                    verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='serialnumber',
            name='computer_set',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       to='hardware.computerset'),
        ),
        migrations.RunPython(update_user)
    ]
