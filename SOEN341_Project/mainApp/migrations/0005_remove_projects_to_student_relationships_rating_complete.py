# Generated by Django 5.0.6 on 2024-10-16 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_rename_myprojects_projects_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects_to_student_relationships',
            name='rating_complete',
        ),
    ]
