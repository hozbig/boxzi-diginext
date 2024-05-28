# Generated by Django 5.0.1 on 2024-01-29 08:43

import content.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_merge_20240129_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیح کوتاه'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='uuid',
            field=models.CharField(blank=True, default=content.models.random_uuid, editable=False, max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='collections',
            field=models.ManyToManyField(to='content.collection', verbose_name='کالکشن های مربوطه'),
        ),
        migrations.AlterField(
            model_name='content',
            name='uuid',
            field=models.CharField(blank=True, default=content.models.random_uuid, editable=False, max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='لینک ویدیو'),
        ),
    ]
