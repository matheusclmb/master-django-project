# Generated by Django 4.0.5 on 2022-06-13 18:51

import coreapp.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('urgency', models.CharField(choices=[('☆', 'Low'), ('☆☆', 'Medium'), ('☆☆☆', 'High'), ('☆☆☆☆', 'Urgent')], max_length=10)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(default=coreapp.models.one_week_calc)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.todolist')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
    ]
