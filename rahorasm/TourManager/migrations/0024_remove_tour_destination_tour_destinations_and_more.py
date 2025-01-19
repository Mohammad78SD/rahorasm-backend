# Generated by Django 5.1.4 on 2025-01-19 07:54

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelManager', '0010_remove_hotelprice_flight_remove_hotelprice_hotel_and_more'),
        ('ReserveManager', '0006_remove_reserve_flight_remove_reserve_hotel'),
        ('TourManager', '0023_flight_arrival_length_flight_departure_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='destination',
        ),
        migrations.AddField(
            model_name='tour',
            name='destinations',
            field=models.ManyToManyField(related_name='tours', to='TourManager.city', verbose_name='مقصد تور'),
        ),
        migrations.AddField(
            model_name='tour',
            name='hotel_price',
            field=models.ManyToManyField(related_name='tour_hotels', to='HotelManager.hotelprice', verbose_name='هتل ها'),
        ),
        migrations.CreateModel(
            name='FlightLeg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', django_jalali.db.models.jDateTimeField(verbose_name='زمان پرواز')),
                ('arrival_time', django_jalali.db.models.jDateTimeField(verbose_name='زمان فرود')),
                ('duration', models.DurationField(verbose_name='مدت زمان پرواز')),
                ('travel_class', models.CharField(choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First', 'First')], max_length=50, verbose_name='کلاس سفر')),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flight_legs', to='TourManager.airline', verbose_name='هواپیمایی')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrival_legs', to='TourManager.airport', verbose_name='فرودگاه مقصد')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departure_legs', to='TourManager.airport', verbose_name='فرودگاه مبدا')),
            ],
        ),
        migrations.AddField(
            model_name='tour',
            name='FlightLegs',
            field=models.ManyToManyField(related_name='flightLegs', to='TourManager.flightleg', verbose_name='پرواز ها'),
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
    ]
