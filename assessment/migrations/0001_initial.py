# Generated by Django 4.2 on 2024-06-20 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.uuid_generator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plan', '0007_remove_plan_has_mvp'),
        ('team', '0013_remove_startupteam_team_members_and_more'),
        ('quiz', '0003_alter_personaltest_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('key_name', models.CharField(max_length=50, verbose_name='نام کلیدی')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'دسته بندی سوال',
                'verbose_name_plural': 'دسته بندی های سوال ها',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('question', models.CharField(max_length=255, verbose_name='سوال')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'سوال',
                'verbose_name_plural': 'سوال ها',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('point', models.PositiveIntegerField(default=0, verbose_name='امتیاز')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individual_of_assessment_response', to=settings.AUTH_USER_MODEL, verbose_name='فرد')),
                ('personal_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_test_of_assessment_response', to='quiz.personaltest', verbose_name='مهارت نرم')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plan_of_assessment_response', to='plan.plan', verbose_name='ایده / محصول')),
                ('pre_register_change', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_register_change_of_assessment_response', to='quiz.preregistertaskresponse', verbose_name='مهارت تخصصی')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_of_assessment_response', to='assessment.question', verbose_name='سوال')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referee_of_assessment_response', to=settings.AUTH_USER_MODEL, verbose_name='داور')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_of_assessment_response', to='team.startupteam', verbose_name='تیم')),
            ],
            options={
                'verbose_name': 'پاسخ',
                'verbose_name_plural': 'پاسخ ها',
            },
        ),
    ]
