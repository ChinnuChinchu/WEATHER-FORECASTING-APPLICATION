# Generated by Django 5.0.2 on 2024-03-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0005_post_reports_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
