# Generated by Django 3.0.4 on 2020-03-16 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0002_auto_20200303_0159"),
    ]

    operations = [
        migrations.AddField(
            model_name="teaminvitation", name="can_delete", field=models.BooleanField(default=True),
        ),
    ]