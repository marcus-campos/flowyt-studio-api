# Generated by Django 3.0.3 on 2020-02-04 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Workspace Name')),
                ('description', models.TextField(blank=True, help_text='(Opcional)', null=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, help_text='(Opcional)', null=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
