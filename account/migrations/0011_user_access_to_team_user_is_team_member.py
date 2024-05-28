# Generated by Django 4.2 on 2024-03-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_remove_startupteam_collections_and_more'),
        ('account', '0010_alter_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_to_team',
            field=models.ManyToManyField(blank=True, to='team.startupteam', verbose_name='دسترسی به تیم'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_team_member',
            field=models.BooleanField(default=False, help_text='آیا این کاربر عضوی از یک تیم استارت آپی هست؟ باید از بخش تیم ها یک یا چند تیم هم برحسب نیاز برایش انتخاب کنید.', verbose_name='عضو تیم'),
        ),
    ]
