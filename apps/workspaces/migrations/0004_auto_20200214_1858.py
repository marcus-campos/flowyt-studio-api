# Generated by Django 3.0.3 on 2020-02-14 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0003_environment_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentrelease',
            name='workspace',
        ),
        migrations.RemoveField(
            model_name='integrationrelease',
            name='workspace',
        ),
    ]