# Generated by Django 4.2 on 2024-06-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_alter_preregistertask_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preregistertaskresponse',
            name='text',
            field=models.TextField(default='', verbose_name='محتوا متنی'),
        ),
    ]
