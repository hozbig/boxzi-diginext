# Generated by Django 4.2 on 2024-03-11 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_startupteam_team_mentors'),
        ('account', '0023_alter_meeting_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_of_meeting', to='team.startupteam', verbose_name='تیم'),
        ),
    ]
