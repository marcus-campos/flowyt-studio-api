# Generated by Django 3.0.3 on 2020-02-15 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0012_auto_20200215_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspace',
            name='slug',
        ),
    ]
