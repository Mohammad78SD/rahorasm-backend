# Generated by Django 5.1.4 on 2025-01-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0029_remove_tour_flight_times_tour_flight_times'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='flight_times',
        ),
        migrations.AddField(
            model_name='tour',
            name='flight_times',
            field=models.ManyToManyField(blank=True, null=True, related_name='tour_flights', to='TourManager.flighttimes', verbose_name='زمان پرواز'),
        ),
    ]
