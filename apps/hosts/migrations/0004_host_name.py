# Generated by Django 3.0.4 on 2020-03-06 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hosts", "0003_auto_20200303_0422"),
    ]

    operations = [
        migrations.AddField(
            model_name="host",
            name="name",
            field=models.CharField(
                blank=True, help_text="(Opcional)", max_length=100, null=True, verbose_name="Name"
            ),
        ),
    ]
