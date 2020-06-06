# Generated by Django 3.0.7 on 2020-06-06 19:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0009_auto_20200606_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='environment_variables',
            field=utils.fields.JSONEncryptedField(blank=True, default=dict, help_text='(Opcional)', null=True, verbose_name='Environment variables'),
        ),
        migrations.AlterField(
            model_name='environmentrelease',
            name='environment_variables',
            field=utils.fields.JSONEncryptedField(blank=True, default=dict, help_text='(Opcional)', null=True, verbose_name='Environment variables'),
        ),
        migrations.AlterField(
            model_name='integration',
            name='integration_variables',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='(Opcional)', null=True, verbose_name='Environment variables'),
        ),
        migrations.AlterField(
            model_name='integrationrelease',
            name='integration_variables',
            field=utils.fields.JSONEncryptedField(blank=True, default=dict, help_text='(Opcional)', null=True, verbose_name='Environment variables'),
        ),
    ]
