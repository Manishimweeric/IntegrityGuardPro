# Generated by Django 5.1.4 on 2025-04-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0013_case_internal_investigator'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='reported_role',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
