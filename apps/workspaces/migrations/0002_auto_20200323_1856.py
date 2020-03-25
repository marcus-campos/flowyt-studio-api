# Generated by Django 3.0.4 on 2020-03-23 18:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("workspaces", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, null=True, verbose_name="Criado em"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, null=True, verbose_name="Atualizado em"
                    ),
                ),
                ("language", models.CharField(max_length=255, verbose_name="Language")),
                ("active", models.BooleanField(default=True, verbose_name="Active?")),
            ],
            options={"verbose_name": "Programming Language", "ordering": ["language"],},
        ),
        migrations.AddField(
            model_name="workspace",
            name="language",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="workspaces.Language"
            ),
        ),
        migrations.AddField(
            model_name="workspacerelease",
            name="language",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="workspaces.Language"
            ),
        ),
    ]