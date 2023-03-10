# Generated by Django 4.1.4 on 2023-01-13 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cers_auth', '0003_alter_cersuser_report_on_behalf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cersuser',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='cersuser',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='company',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='company',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='department',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='department',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
    ]
