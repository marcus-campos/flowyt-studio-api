# Generated by Django 3.0.3 on 2020-02-08 20:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Environment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Environment Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "environment_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.CreateModel(
            name="Flow",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Flow Name")),
                (
                    "flow_layout",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        verbose_name="Flow Layout"
                    ),
                ),
                (
                    "flow_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Flow Data",
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
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Function Name"),
                ),
                (
                    "function_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
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
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Integration Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "integration_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
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
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Workspace Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
            ],
            options={"ordering": ["updated_at"],},
        ),
        migrations.CreateModel(
            name="Workspace",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Workspace Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "workspace_color",
                    models.CharField(
                        blank=True,
                        max_length=6,
                        null=True,
                        verbose_name="Workspace Name",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="WorkspaceRelease",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Workspace Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "workspace_color",
                    models.CharField(
                        blank=True,
                        max_length=6,
                        null=True,
                        verbose_name="Workspace Name",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Release",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Workspace",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.AddField(
            model_name="release",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"
            ),
        ),
        migrations.CreateModel(
            name="IntegrationRelease",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Integration Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "integration_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
                    ),
                ),
                (
                    "integration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Integration",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Release",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Workspace",
                    ),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.WorkspaceRelease",
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="integration",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"
            ),
        ),
        migrations.CreateModel(
            name="FunctionFileRelease",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Function Name"),
                ),
                (
                    "function_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
                    ),
                ),
                (
                    "function_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.FunctionFile",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Release",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Workspace",
                    ),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.WorkspaceRelease",
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="functionfile",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"
            ),
        ),
        migrations.CreateModel(
            name="FlowRelease",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Flow Name")),
                (
                    "flow_layout",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        verbose_name="Flow Layout"
                    ),
                ),
                (
                    "flow_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Flow Data",
                    ),
                ),
                (
                    "flow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Flow",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Release",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Workspace",
                    ),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.WorkspaceRelease",
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.AddField(
            model_name="flow",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"
            ),
        ),
        migrations.CreateModel(
            name="EnvironmentRelease",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Criado em",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        db_index=True,
                        null=True,
                        verbose_name="Atualizado em",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Environment Name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "environment_variables",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        help_text="(Opcional)",
                        null=True,
                        verbose_name="Environment variables",
                    ),
                ),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Environment",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Release",
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.Workspace",
                    ),
                ),
                (
                    "workspace_release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspaces.WorkspaceRelease",
                    ),
                ),
            ],
            options={"ordering": ["created_at"],},
        ),
        migrations.AddField(
            model_name="environment",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="workspaces.Workspace"
            ),
        ),
    ]
