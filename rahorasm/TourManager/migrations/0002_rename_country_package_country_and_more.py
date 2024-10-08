# Generated by Django 5.1 on 2024-09-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourManager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='Country',
            new_name='country',
        ),
        migrations.AlterField(
            model_name='airline',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
