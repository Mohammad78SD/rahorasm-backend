# Generated by Django 5.1 on 2024-10-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0008_remove_tour_package_rename_price_tour_least_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='least_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
