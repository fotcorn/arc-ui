# Generated by Django 5.0.6 on 2024-06-23 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('train', models.JSONField()),
                ('test', models.JSONField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.dataset')),
            ],
        ),
    ]
