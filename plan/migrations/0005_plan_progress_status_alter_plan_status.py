# Generated by Django 4.2 on 2024-06-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0004_plan_pitch_deck'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='progress_status',
            field=models.CharField(choices=[('0', 'در حال توسعه نسخه MVP هستیم'), ('1', 'نسخه MVP آماده داریم'), ('2', 'محصول آماده به کار داریم'), ('3', 'قبلا محصول خود را به بازار ارایه کرده\u200cایم')], default='i', max_length=1, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='status',
            field=models.CharField(choices=[('i', 'فقط دارای ایده هستم'), ('m', 'دارای یک محصول هستم')], default='i', max_length=1, verbose_name='وضعیت'),
        ),
    ]