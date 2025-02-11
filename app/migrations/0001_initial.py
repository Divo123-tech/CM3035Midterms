# Generated by Django 5.1.4 on 2024-12-11 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=3)),
                ('payroll', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('salary', models.IntegerField()),
                ('free_agent', models.BooleanField(default=False)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team')),
            ],
        ),
    ]
