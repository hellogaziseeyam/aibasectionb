# Generated by Django 5.2 on 2025-04-11 10:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('A', 'Section A'), ('B', 'Section B')], default='B', max_length=1)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('A', 'Section A'), ('B', 'Section B')], default='B', max_length=1)),
                ('course_name', models.CharField(choices=[('Functional English', 'Functional English'), ('Computer and its Application', 'Computer and its Application'), ('Presentation Skill Development', 'Presentation Skill Development'), ('Principles of Management', 'Principles of Management'), ('Environmental Studies', 'Environmental Studies')], max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('document', models.FileField(blank=True, null=True, upload_to='assignment_docs/')),
                ('due_date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-due_date'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('cr', 'Class Representative'), ('student', 'Student')], max_length=10)),
                ('section', models.CharField(choices=[('A', 'Section A'), ('B', 'Section B')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('A', 'Section A'), ('B', 'Section B')], default='B', max_length=1)),
                ('course_name', models.CharField(choices=[('Functional English', 'Functional English'), ('Computer and its Application', 'Computer and its Application'), ('Presentation Skill Development', 'Presentation Skill Development'), ('Principles of Management', 'Principles of Management'), ('Environmental Studies', 'Environmental Studies')], max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('syllabus', models.TextField()),
                ('document', models.FileField(blank=True, null=True, upload_to='quiz_docs/')),
                ('date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
