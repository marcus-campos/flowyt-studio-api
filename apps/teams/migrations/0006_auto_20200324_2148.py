# Generated by Django 3.0.4 on 2020-03-24 21:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0005_teaminvitation_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="organization",
            field=models.CharField(default="Personal", max_length=255, verbose_name="Organization"),
        ),
        migrations.AlterField(
            model_name="teaminvitation",
            name="status",
            field=models.IntegerField(
                choices=[(0, "PENDING"), (1, "ACCEPTED"), (2, "DECLINED"), (4, "EXPIRED"), (5, "REMOVED")],
                default=0,
            ),
        ),
        migrations.CreateModel(
            name="SubDomain",
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
                ("sub_domain", models.URLField(max_length=500, verbose_name="Sub Domain")),
                ("active", models.BooleanField(default=True, verbose_name="Active?")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.Team")),
            ],
            options={"ordering": ["team", "sub_domain"],},
        ),
    ]
