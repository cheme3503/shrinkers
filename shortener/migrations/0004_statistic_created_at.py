# Generated by Django 3.1.1 on 2023-01-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_users_telegram_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
