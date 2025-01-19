# Generated by Django 5.1.4 on 2025-01-19 12:44

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelManager', '0010_remove_hotelprice_flight_remove_hotelprice_hotel_and_more'),
        ('TourManager', '0025_remove_flightleg_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='FlightLegs',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='hotel_price',
        ),
        migrations.CreateModel(
            name='FlightTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', django_jalali.db.models.jDateTimeField(verbose_name='زمان پرواز')),
                ('arrival_time', django_jalali.db.models.jDateTimeField(verbose_name='زمان فرود')),
                ('flight_Legs', models.ManyToManyField(related_name='flightLegs', to='TourManager.flightleg', verbose_name='پرواز ها')),
                ('hotel_price', models.ManyToManyField(related_name='tour_hotels', to='HotelManager.hotelprice', verbose_name='هتل ها')),
            ],
            options={
                'verbose_name': 'زمان پرواز',
                'verbose_name_plural': 'زمان های پرواز',
            },
        ),
        migrations.AddField(
            model_name='tour',
            name='flight_times',
            field=models.ManyToManyField(related_name='tour_flights', to='TourManager.flighttimes', verbose_name='زمان پرواز'),
        ),
    ]
