# Generated by Django 4.2 on 2024-06-09 06:48

from django.db import migrations, models
import plan.models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_plan_video_alter_plan_has_mvp'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='pitch_deck',
            field=models.FileField(blank=True, null=True, upload_to=plan.models.pitch_deck_directory_path, verbose_name='آپلود فایل pitch deck'),
        ),
    ]
