# Generated by Django 4.2 on 2024-04-13 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.uuid_generator


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0041_road_holders_road_sponsors'),
        ('team', '0006_startupteam_team_mentors'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('status', models.CharField(choices=[('w', 'در انتظار برسی'), ('p', 'فعال'), ('a', 'تایید شده'), ('r', 'رد شده'), ('c', 'نیاز به برسی')], default='w', max_length=1, verbose_name='شیوه برگزاری')),
                ('client_last_response_date', models.DateField(verbose_name='زمان آخرین تغییر توسط کاربر')),
                ('accelerator_last_response_date', models.DateField(verbose_name='زمان آخرین واکنش توسط شتابدهنده')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='زمان آخرین بروزرسانی')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Road_of_road_registration', to='content.road', verbose_name='مسیر')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_of_road_registration', to='team.startupteam', verbose_name='تیم')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_of_road_registration', to=settings.AUTH_USER_MODEL, verbose_name='تیم')),
            ],
            options={
                'verbose_name': 'ثبت نام مسیر آموزشی',
                'verbose_name_plural': 'ثبت نام مسیرهای آموزشی',
            },
        ),
    ]
