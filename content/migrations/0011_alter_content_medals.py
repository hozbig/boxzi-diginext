# Generated by Django 4.2 on 2024-02-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_content_medals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='medals',
            field=models.PositiveIntegerField(default=0, verbose_name='مدال'),
        ),
    ]
