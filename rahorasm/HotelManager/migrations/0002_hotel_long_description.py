# Generated by Django 5.1 on 2024-11-10 08:23

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HotelManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='long_description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Text'),
        ),
    ]
