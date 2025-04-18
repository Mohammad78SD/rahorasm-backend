# Generated by Django 5.1 on 2024-11-10 13:11

import django.db.models.deletion
import django_ckeditor_5.fields
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelManager', '0002_hotel_long_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='long_description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیح بیشتر'),
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotel_images/')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_images', to='HotelManager.hotel')),
            ],
            options={
                'verbose_name': 'تصویر هتل',
                'verbose_name_plural': 'تصاویر هتل',
            },
        ),
    ]
