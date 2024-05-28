# Generated by Django 4.2 on 2024-03-14 12:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0006_startupteam_team_mentors'),
        ('company', '0009_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='mentors',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='مربی ها'),
        ),
        migrations.AddField(
            model_name='center',
            name='teams',
            field=models.ManyToManyField(blank=True, to='team.startupteam', verbose_name='تیم های استارتاپی'),
        ),
    ]
