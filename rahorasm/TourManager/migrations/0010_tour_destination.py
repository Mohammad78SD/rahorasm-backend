# Generated by Django 5.1 on 2024-10-22 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0009_alter_tour_least_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='destination',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='TourManager.city'),
            preserve_default=False,
        ),
    ]
