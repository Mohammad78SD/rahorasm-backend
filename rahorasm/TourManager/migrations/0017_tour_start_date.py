# Generated by Django 5.1 on 2024-11-06 12:32

import django_jalali.db.models
import jdatetime
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0016_tour_max_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='start_date',
            field=django_jalali.db.models.jDateField(default=jdatetime.date.today),
        ),
    ]
