# Generated by Django 5.1.4 on 2024-12-24 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrityGuard_app', '0004_alter_user_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collabration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reciever_email', models.CharField(blank=True, max_length=100)),
                ('message', models.TextField(blank=True, max_length=100)),
                ('sender_email', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
