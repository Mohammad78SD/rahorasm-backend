# Generated by Django 5.1 on 2024-09-23 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VisaManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'سوال و جواب ویزا', 'verbose_name_plural': 'سوالات و جواب های ویزا'},
        ),
        migrations.AlterModelOptions(
            name='visa',
            options={'verbose_name': 'ویزا', 'verbose_name_plural': 'ویزاها'},
        ),
    ]