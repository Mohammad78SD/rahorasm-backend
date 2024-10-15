# Generated by Django 5.1 on 2024-10-15 19:06

import django.db.models.deletion
import django_ckeditor_5.fields
import django_jalali.db.models
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[40, 40], upload_to='./logo')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'هواپیمایی',
                'verbose_name_plural': 'هواپیمایی ها',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهر ها',
            },
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'قاره',
                'verbose_name_plural': 'قاره ها',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=10)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='TourManager.city')),
            ],
            options={
                'verbose_name': 'فرودگاه',
                'verbose_name_plural': 'فرودگاه ها',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='continents', to='TourManager.continent')),
            ],
            options={
                'verbose_name': 'کشور',
                'verbose_name_plural': 'کشور ها',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='counteris', to='TourManager.country'),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('rahvarasm', models.CharField(max_length=255, verbose_name='صفر با راه و رسم')),
                ('besttime', models.CharField(max_length=255, verbose_name='بهترین زمان سفر')),
                ('porsCons', models.CharField(max_length=255, verbose_name='مزایا و معایب ')),
                ('atrraction', models.CharField(max_length=255, verbose_name='جاذبه')),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('land', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='سفر با راه و رسم')),
                ('ProsCons', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='مزایا و  معایب')),
                ('attraction', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='جاذبه های تورسیتی')),
                ('Bestime', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='بهترین زمان')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='TourManager.city')),
            ],
            options={
                'verbose_name': 'پکیج',
                'verbose_name_plural': 'پکیج ها',
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('tour_type', models.CharField(choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی')], max_length=200)),
                ('is_featured', models.BooleanField(default=False)),
                ('tour_duration', models.CharField(default='7 روز', max_length=200)),
                ('needed_documents', models.TextField()),
                ('agency_service', models.TextField()),
                ('tour_guide', models.TextField()),
                ('start_date', django_jalali.db.models.jDateTimeField()),
                ('end_date', django_jalali.db.models.jDateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('edited_at', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='TourManager.airline')),
                ('destination_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination_airport', to='TourManager.airport')),
                ('origin_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_airport', to='TourManager.airport')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tours', to='TourManager.package')),
            ],
            options={
                'verbose_name': 'تور',
                'verbose_name_plural': 'تور ها',
            },
        ),
    ]
