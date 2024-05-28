# Generated by Django 4.2 on 2024-04-06 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0031_alter_collection_accelerator_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'verbose_name': 'فصل آموزشی', 'verbose_name_plural': 'فصل های'},
        ),
        migrations.AlterModelOptions(
            name='collectionorder',
            options={'ordering': ['row_number'], 'verbose_name': 'ترتیب فصل', 'verbose_name_plural': 'ترتیب فصل ها'},
        ),
        migrations.AlterField(
            model_name='collectionorder',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_of_collection_order', to='content.collection', verbose_name='فصل'),
        ),
    ]
