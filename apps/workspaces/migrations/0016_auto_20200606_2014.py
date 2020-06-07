# Generated by Django 3.0.7 on 2020-06-06 20:14

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("workspaces", "0015_auto_20200606_2013"),
    ]

    operations = [
        migrations.AlterField(
            model_name="environment",
            name="environment_variables",
            field=utils.fields.JSONEncryptedField(
                blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
            ),
        ),
        migrations.AlterField(
            model_name="environmentrelease",
            name="environment_variables",
            field=utils.fields.JSONEncryptedField(
                blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
            ),
        ),
        migrations.AlterField(
            model_name="integration",
            name="integration_variables",
            field=utils.fields.JSONEncryptedField(
                blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
            ),
        ),
        migrations.AlterField(
            model_name="integrationrelease",
            name="integration_variables",
            field=utils.fields.JSONEncryptedField(
                blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
            ),
        ),
    ]