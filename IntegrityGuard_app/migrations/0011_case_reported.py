# Generated by Django 5.1.4 on 2025-02-06 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0010_case_legal_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='reported',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
