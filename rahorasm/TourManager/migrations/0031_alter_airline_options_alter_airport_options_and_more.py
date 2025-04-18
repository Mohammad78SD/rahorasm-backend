# Generated by Django 5.1.4 on 2025-01-29 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0030_remove_tour_flight_times_tour_flight_times'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airline',
            options={'verbose_name': 'هواپیمایی', 'verbose_name_plural': '6. هواپیمایی ها'},
        ),
        migrations.AlterModelOptions(
            name='airport',
            options={'verbose_name': 'فرودگاه', 'verbose_name_plural': '5. فرودگاه ها'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'شهر', 'verbose_name_plural': '4. شهر ها'},
        ),
        migrations.AlterModelOptions(
            name='continent',
            options={'verbose_name': 'قاره', 'verbose_name_plural': '2. قاره ها'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'کشور', 'verbose_name_plural': '3. کشور ها'},
        ),
        migrations.AlterModelOptions(
            name='flightleg',
            options={'verbose_name': 'پرواز', 'verbose_name_plural': 'پرواز ها'},
        ),
        migrations.AlterModelOptions(
            name='tour',
            options={'verbose_name': 'تور', 'verbose_name_plural': '1. تور ها'},
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_duration',
            field=models.IntegerField(default=3, verbose_name='مدت زمان تور (شب)'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_type',
            field=models.CharField(choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی'), ('دریایی', 'دریایی')], max_length=200, verbose_name='نوع تور'),
        ),
    ]
