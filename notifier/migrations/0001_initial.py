# Generated by Django 4.2 on 2024-06-18 22:11

from django.db import migrations, models
import utils.uuid_generator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('status', models.CharField(max_length=3, verbose_name='کد وضعیت')),
                ('message', models.JSONField(null=True, verbose_name='پاسخ سرور')),
                ('send_try', models.PositiveIntegerField(verbose_name='تلاش برای ارسال')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='زمان آخرین بروزرسانی')),
            ],
        ),
    ]