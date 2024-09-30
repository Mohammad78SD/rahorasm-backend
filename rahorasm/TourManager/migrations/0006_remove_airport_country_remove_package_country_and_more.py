# Generated by Django 5.1 on 2024-09-30 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0005_alter_city_country_alter_country_continent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airport',
            name='country',
        ),
        migrations.RemoveField(
            model_name='package',
            name='country',
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='cities', to='TourManager.country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='countries', to='TourManager.continent'),
            preserve_default=False,
        ),
    ]
