# Generated by Django 5.1.4 on 2025-02-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0009_mainpagepdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutdetail',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
        migrations.AddField(
            model_name='contactdetail',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='ترتیب نمایش'),
        ),
    ]
