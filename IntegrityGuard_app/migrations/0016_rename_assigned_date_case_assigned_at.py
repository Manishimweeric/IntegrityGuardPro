# Generated by Django 5.1.4 on 2025-04-28 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0015_case_assigned_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='Assigned_date',
            new_name='Assigned_at',
        ),
    ]
