# Generated by Django 3.1.1 on 2023-01-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_backofficelogs_status_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='device_os',
            field=models.CharField(max_length=30),
        ),
    ]
