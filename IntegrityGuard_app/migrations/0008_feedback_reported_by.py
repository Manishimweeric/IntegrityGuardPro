# Generated by Django 5.1.4 on 2024-12-25 01:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0007_remove_feedback_feedback_text_feedback_feedback_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='reported_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='IntegrityGuard_app.user'),
            preserve_default=False,
        ),
    ]
