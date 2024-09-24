# Generated by Django 5.1 on 2024-09-23 07:56

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0003_rename_air_line_tour_airline'),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='airline',
            options={'verbose_name': 'هواپیمایی', 'verbose_name_plural': 'هواپیمایی ها'},
        ),
        migrations.AlterModelOptions(
            name='airport',
            options={'verbose_name': 'فرودگاه', 'verbose_name_plural': 'فرودگاه ها'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'شهر', 'verbose_name_plural': 'شهر ها'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'کشور', 'verbose_name_plural': 'کشور ها'},
        ),
        migrations.AlterModelOptions(
            name='package',
            options={'verbose_name': 'پکیج', 'verbose_name_plural': 'پکیج ها'},
        ),
        migrations.AlterModelOptions(
            name='tour',
            options={'verbose_name': 'تور', 'verbose_name_plural': 'تور ها'},
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='TourManager.country'),
        ),
        migrations.AddField(
            model_name='tour',
            name='tour_duration',
            field=models.CharField(default='7 روز', max_length=200),
        ),
        migrations.AlterField(
            model_name='tour',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tours', to='TourManager.package'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='tour_type',
            field=models.CharField(choices=[('هوایی', 'هوایی'), ('زمینی', 'زمینی')], max_length=200),
        ),
        migrations.AddField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='TourManager.continent'),
        ),
    ]