# Generated by Django 3.0.7 on 2020-06-07 00:07

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0020_auto_20200607_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='environment_variables',
            field=utils.fields.JSONEncryptedField(blank=True, help_text='(Opcional)', null=True, verbose_name='Environment variables'),
        ),
    ]
