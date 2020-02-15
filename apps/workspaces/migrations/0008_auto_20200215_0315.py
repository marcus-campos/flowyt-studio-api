# Generated by Django 3.0.3 on 2020-02-15 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0007_release_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environment',
            name='active',
        ),
        migrations.AddField(
            model_name='environment',
            name='debug',
            field=models.BooleanField(default=False, help_text='(Default false)'),
        ),
    ]
