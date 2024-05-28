# Generated by Django 4.2 on 2024-03-04 13:18

from django.db import migrations, models
import django.db.models.deletion
import plan.models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_remove_startupteam_plan'),
        ('plan', '0007_idea_delete_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=plan.models.random_uuid, editable=False, max_length=5, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='plan/logo/', verbose_name='لوگو')),
                ('name', models.CharField(max_length=255, verbose_name='نام طرح')),
                ('industry', models.CharField(max_length=255, verbose_name='صنعت')),
                ('state', models.CharField(max_length=255, verbose_name='استان')),
                ('city', models.CharField(max_length=255, verbose_name='شهر')),
                ('description', models.TextField(verbose_name='توصیف طرح')),
                ('has_mvp', models.BooleanField(verbose_name='دارای کمینه')),
                ('status', models.CharField(choices=[('p', 'درحال انجام'), ('f', 'تمام شده')], default='p', max_length=1, verbose_name='وضعیت')),
                ('telegram', models.URLField(blank=True, max_length=255, null=True, verbose_name='تلگرام')),
                ('instagram', models.URLField(blank=True, max_length=255, null=True, verbose_name='اینستاگرام')),
                ('twitter', models.URLField(blank=True, max_length=255, null=True, verbose_name='توئیتر (ایکس)')),
                ('linkdin', models.URLField(blank=True, max_length=255, null=True, verbose_name='لینکدین')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_plan', to='team.startupteam', verbose_name='تیم')),
            ],
            options={
                'verbose_name': 'طرح',
                'verbose_name_plural': 'طرح ها',
            },
        ),
        migrations.DeleteModel(
            name='Idea',
        ),
    ]
