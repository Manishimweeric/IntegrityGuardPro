# Generated by Django 5.1.4 on 2025-04-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0014_feedback_reported_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='Assigned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
