# Generated by Django 5.1.4 on 2025-01-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0022_alter_tour_description_editor'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='arrival_length',
            field=models.DurationField(blank=True, null=True, verbose_name='مدت زمان پرواز برگشت'),
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_length',
            field=models.DurationField(blank=True, null=True, verbose_name='مدت زمان پرواز رفت'),
        ),
    ]
