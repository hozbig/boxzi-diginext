# Generated by Django 4.2 on 2024-03-14 12:18

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_center_mentors_center_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='description',
            field=django_quill.fields.QuillField(blank=True, default='', verbose_name='توضیحات'),
        ),
    ]
