# Generated by Django 4.2 on 2024-06-24 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0004_alter_notifylog_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifylog',
            name='action',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='اسم عملیات'),
        ),
    ]
