# Generated by Django 4.2 on 2024-02-26 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plan.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=plan.models.random_uuid, editable=False, max_length=5, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/logo/', verbose_name='لوگو')),
                ('name', models.CharField(max_length=255, verbose_name='نام طرح')),
                ('industry', models.CharField(max_length=255, verbose_name='صنعت')),
                ('state', models.CharField(max_length=255, verbose_name='استان')),
                ('city', models.CharField(max_length=255, verbose_name='شهر')),
                ('description', models.TextField(verbose_name='توصیف طرح')),
                ('has_mvp', models.BooleanField(verbose_name='دارای کمینه')),
                ('has_team', models.BooleanField(verbose_name='دارای تیم')),
                ('telegram', models.URLField(max_length=255, verbose_name='تلگرام')),
                ('instagram', models.URLField(max_length=255, verbose_name='اینستاگرام')),
                ('twitter', models.URLField(max_length=255, verbose_name='توئیتر (ایکس)')),
                ('linkdin', models.URLField(max_length=255, verbose_name='لینکدین')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_plan', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'طرح',
                'verbose_name_plural': 'طرح ها',
            },
        ),
    ]
