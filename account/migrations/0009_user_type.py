# Generated by Django 4.2 on 2024-02-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_user_received_medals'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('c', 'کنجکاو'), ('e', 'کارآفرین')], default='c', max_length=1, verbose_name='نوع کاربر'),
        ),
    ]
