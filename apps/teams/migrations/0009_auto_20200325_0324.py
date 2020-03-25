# Generated by Django 3.0.4 on 2020-03-25 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0008_team_is_personal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="is_personal",
            field=models.BooleanField(default=False, verbose_name="Is Personal Team?"),
        ),
    ]