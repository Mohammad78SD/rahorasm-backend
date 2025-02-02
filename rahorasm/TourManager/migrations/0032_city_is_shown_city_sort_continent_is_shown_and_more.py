# Generated by Django 5.1.4 on 2025-02-02 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0031_alter_airline_options_alter_airport_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='is_shown',
            field=models.BooleanField(default=True, verbose_name='آیا در منو نمایش داده شود؟'),
        ),
        migrations.AddField(
            model_name='city',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
        migrations.AddField(
            model_name='continent',
            name='is_shown',
            field=models.BooleanField(default=True, verbose_name='آیا در منو نمایش داده شود؟'),
        ),
        migrations.AddField(
            model_name='continent',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
        migrations.AddField(
            model_name='country',
            name='is_shown',
            field=models.BooleanField(default=True, verbose_name='آیا در منو نمایش داده شود؟'),
        ),
        migrations.AddField(
            model_name='country',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='آیا ویژه است؟'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='is_shown',
            field=models.BooleanField(default=True, verbose_name='آیا اعتبار دارد؟'),
        ),
    ]
