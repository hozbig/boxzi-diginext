# Generated by Django 5.0.1 on 2024-01-29 06:38

import content.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_content_collections_delete_contentcollection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='uuid',
            field=models.UUIDField(blank=True, default=content.models.random_uuid, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='collections',
            field=models.ManyToManyField(null=True, to='content.collection', verbose_name='کالکشن های مربوطه'),
        ),
        migrations.AlterField(
            model_name='content',
            name='uuid',
            field=models.UUIDField(blank=True, default=content.models.random_uuid, editable=False, unique=True),
        ),
    ]
