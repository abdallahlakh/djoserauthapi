# Generated by Django 4.2.1 on 2024-03-19 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mouhami_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mouhami_api.customer')),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mouhami_api.lawyer')),
            ],
        ),
    ]
