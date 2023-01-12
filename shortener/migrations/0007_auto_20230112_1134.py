# Generated by Django 3.1.1 on 2023-01-12 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0006_auto_20230112_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=50)),
                ('flag_name', models.CharField(max_length=50)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='statistic',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 5, 11, 34, 34, 694798)),
        ),
        migrations.AlterField(
            model_name='users',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]