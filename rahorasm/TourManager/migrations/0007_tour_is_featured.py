# Generated by Django 5.1 on 2024-10-04 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0006_remove_airport_country_remove_package_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
