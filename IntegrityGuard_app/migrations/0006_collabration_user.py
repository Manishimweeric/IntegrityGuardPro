# Generated by Django 5.1.4 on 2024-12-24 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0005_collabration'),
    ]

    operations = [
        migrations.AddField(
            model_name='collabration',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='IntegrityGuard_app.user'),
            preserve_default=False,
        ),
    ]
