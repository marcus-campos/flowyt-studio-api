# Generated by Django 3.0.4 on 2020-03-11 00:57

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0002_auto_20200303_0159"),
    ]

    operations = [
        migrations.CreateModel(
            name="Environment",
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
                ("name", models.CharField(max_length=255, verbose_name="Environment Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "environment_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
                ("debug", models.BooleanField(default=False, help_text="(Default false)")),
                (
                    "safe_mode",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
                ("can_delete", models.BooleanField(default=True)),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.CreateModel(
            name="Flow",
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
                ("name", models.CharField(max_length=255, verbose_name="Flow Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "flow_layout",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Flow Layout"
                    ),
                ),
                (
                    "flow_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Flow Data"
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="FlowRelease",
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
                ("name", models.CharField(max_length=255, verbose_name="Flow Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                ("flow_layout", django.contrib.postgres.fields.jsonb.JSONField(verbose_name="Flow Layout")),
                (
                    "flow_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Flow Data"
                    ),
                ),
                (
                    "flow",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.Flow",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="FunctionFile",
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
                ("name", models.CharField(max_length=255, verbose_name="Function Name")),
                (
                    "function_data",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Function data"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.CreateModel(
            name="Integration",
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
                ("name", models.CharField(max_length=255, verbose_name="Integration Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "integration_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.CreateModel(
            name="Release",
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
                ("name", models.CharField(max_length=255, verbose_name="Workspace Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                ("published", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"],},
        ),
        migrations.CreateModel(
            name="Route",
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
                ("path", models.CharField(max_length=255, verbose_name="Path")),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("GET", "Get"),
                            ("POST", "Post"),
                            ("PUT", "Put"),
                            ("DELETE", "Delete"),
                            ("PATCH", "Patch"),
                            ("TRACE", "Trace"),
                            ("OPTIONS", "Options"),
                            ("CONNECT", "Connect"),
                        ],
                        max_length=10,
                        verbose_name="HTTP Method",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "flow",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Flow"),
                ),
            ],
            options={"ordering": ["path"],},
        ),
        migrations.CreateModel(
            name="Workspace",
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
                ("name", models.CharField(max_length=255, verbose_name="Workspace Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "workspace_color",
                    models.CharField(blank=True, max_length=7, null=True, verbose_name="Workspace Color"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.Team")),
            ],
            options={"ordering": ["name"], "unique_together": {("name", "team")},},
        ),
        migrations.CreateModel(
            name="WorkspaceRelease",
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
                ("name", models.CharField(max_length=255, verbose_name="Workspace Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "workspace_color",
                    models.CharField(blank=True, max_length=6, null=True, verbose_name="Workspace Color"),
                ),
                (
                    "release",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.Workspace",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="RouteRelease",
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
                ("path", models.CharField(max_length=255, verbose_name="Path")),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("GET", "Get"),
                            ("POST", "Post"),
                            ("PUT", "Put"),
                            ("DELETE", "Delete"),
                            ("PATCH", "Patch"),
                            ("TRACE", "Trace"),
                            ("OPTIONS", "Options"),
                            ("CONNECT", "Connect"),
                        ],
                        max_length=10,
                        verbose_name="HTTP Method",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "flow_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workspaces.FlowRelease"
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
                ),
                (
                    "route",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.Route",
                    ),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workspaces.WorkspaceRelease"
                    ),
                ),
            ],
            options={"ordering": ["path"],},
        ),
        migrations.AddField(
            model_name="route",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.AddField(
            model_name="release",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.CreateModel(
            name="IntegrationRelease",
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
                ("name", models.CharField(max_length=255, verbose_name="Integration Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "integration_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
                (
                    "integration",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.Integration",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workspaces.WorkspaceRelease"
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="integration",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.CreateModel(
            name="FunctionFileRelease",
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
                ("name", models.CharField(max_length=255, verbose_name="Function Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "function_data",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Function data"
                    ),
                ),
                (
                    "function_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.FunctionFile",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workspaces.WorkspaceRelease"
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="functionfile",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.AddField(
            model_name="flowrelease",
            name="release",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
        ),
        migrations.AddField(
            model_name="flowrelease",
            name="workspace_release",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.WorkspaceRelease"
            ),
        ),
        migrations.AddField(
            model_name="flow",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.CreateModel(
            name="EnvironmentRelease",
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
                ("name", models.CharField(max_length=255, verbose_name="Environment Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Description"
                    ),
                ),
                (
                    "environment_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
                ("debug", models.BooleanField(default=False, help_text="(Default false)")),
                (
                    "safe_mode",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, help_text="(Opcional)", null=True, verbose_name="Environment variables"
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="workspaces.Environment",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Release"),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="workspaces.WorkspaceRelease"
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="environment",
            name="workspace",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"),
        ),
        migrations.AlterUniqueTogether(name="route", unique_together={("path", "method", "workspace")},),
        migrations.AlterUniqueTogether(name="release", unique_together={("name", "workspace")},),
        migrations.AlterUniqueTogether(name="integration", unique_together={("name", "workspace")},),
        migrations.AlterUniqueTogether(name="functionfile", unique_together={("name", "workspace")},),
        migrations.AlterUniqueTogether(name="flow", unique_together={("name", "workspace")},),
        migrations.AlterUniqueTogether(name="environment", unique_together={("name", "workspace")},),
    ]
