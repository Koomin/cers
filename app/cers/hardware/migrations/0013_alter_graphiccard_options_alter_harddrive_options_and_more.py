# Generated by Django 4.1.4 on 2023-01-27 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0012_rename_motherboard_motherboardmodel_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='graphiccard',
            options={'verbose_name': 'Graphic Card', 'verbose_name_plural': 'Graphic Cards'},
        ),
        migrations.AlterModelOptions(
            name='harddrive',
            options={'verbose_name': 'Hard Drive', 'verbose_name_plural': 'Hard Drive'},
        ),
        migrations.AlterModelOptions(
            name='harddrivemodel',
            options={'verbose_name': 'Hard Drive', 'verbose_name_plural': 'Hard Drive'},
        ),
        migrations.AlterModelOptions(
            name='memory',
            options={'verbose_name': 'Memory', 'verbose_name_plural': 'Memories'},
        ),
        migrations.AlterModelOptions(
            name='memorymodel',
            options={'verbose_name': 'Memory', 'verbose_name_plural': 'Memory'},
        ),
    ]
