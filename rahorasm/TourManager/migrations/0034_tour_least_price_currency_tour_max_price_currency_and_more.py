# Generated by Django 5.1.4 on 2025-02-05 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0033_flightleg_flight_length_flightleg_leg_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='least_price_currency',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='نرخ ارزی کمترین قیمت تور'),
        ),
        migrations.AddField(
            model_name='tour',
            name='max_price_currency',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='نرخ ارزی بیشترین قیمت تور'),
        ),
        migrations.AddField(
            model_name='tour',
            name='other_currency',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ارز دیگر'),
        ),
    ]
