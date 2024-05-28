# Generated by Django 4.2 on 2024-04-06 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0032_alter_collection_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='road',
            name='expiration_date',
            field=models.DateField(null=True, verbose_name='تاریخ انقضا'),
        ),
        migrations.AddField(
            model_name='road',
            name='start_date',
            field=models.DateField(null=True, verbose_name='تاریخ شروع'),
        ),
    ]
