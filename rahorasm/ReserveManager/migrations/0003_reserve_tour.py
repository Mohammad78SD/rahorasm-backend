# Generated by Django 5.1 on 2024-11-13 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReserveManager', '0002_remove_person_age_alter_person_birth_date'),
        ('TourManager', '0017_tour_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='tour',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='TourManager.tour'),
            preserve_default=False,
        ),
    ]
