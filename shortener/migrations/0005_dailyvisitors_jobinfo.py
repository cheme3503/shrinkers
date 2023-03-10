# Generated by Django 3.1.1 on 2023-01-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0004_auto_20230115_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyVisitors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField()),
                ('visits', models.IntegerField(default=0)),
                ('totals', models.IntegerField(default=0)),
                ('last_updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=255)),
                ('user_id', models.IntegerField(null=True)),
                ('additional_info', models.JSONField(null=True)),
                ('status', models.CharField(choices=[('wait', 'Wait'), ('run', 'Run'), ('ok', 'Ok'), ('error', 'Error')], default='wait', max_length=6)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
