# Generated by Django 4.2.1 on 2024-03-22 16:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mouhami_api', '0011_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='review',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
