# Generated by Django 4.1.4 on 2023-01-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0002_alter_computer_created_alter_computer_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
