# Generated by Django 4.2 on 2024-04-23 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0021_alter_teammember_user_validation_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plan', '0010_alter_plan_options_alter_plan_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='city',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='linkdin',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='state',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='telegram',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='twitter',
        ),
        migrations.AddField(
            model_name='plan',
            name='likes',
            field=models.ManyToManyField(related_name='user_of_likes_plan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plan',
            name='text',
            field=django_quill.fields.QuillField(default='', verbose_name='توضیحات کامل'),
        ),
        migrations.AddField(
            model_name='plan',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_of_plan', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=models.TextField(verbose_name='توصیف کوتاه'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_of_plan', to='team.startupteam', verbose_name='تیم'),
        ),
    ]
