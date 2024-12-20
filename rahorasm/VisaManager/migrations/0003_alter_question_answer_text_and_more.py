# Generated by Django 5.1 on 2024-12-16 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VisaManager', '0002_alter_question_options_alter_visa_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_text',
            field=models.TextField(verbose_name='پاسخ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=255, verbose_name='سوال'),
        ),
        migrations.AlterField(
            model_name='question',
            name='visa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='VisaManager.visa', verbose_name='ویزا'),
        ),
        migrations.AlterField(
            model_name='visa',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='visa',
            name='title',
            field=models.CharField(max_length=200, verbose_name='نام کشور'),
        ),
    ]
