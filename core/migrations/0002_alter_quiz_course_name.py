# Generated by Django 5.2 on 2025-04-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='course_name',
            field=models.CharField(choices=[('Functional English', 'Functional English'), ('Computer and its Application', 'Computer and its Application'), ('Presentation Skill Development', 'Presentation Skill Development'), ('Principles of Management', 'Principles of Management'), ('Environmental Studies', 'Environmental Studies')], max_length=200),
        ),
    ]
