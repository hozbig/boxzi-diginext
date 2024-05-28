# Generated by Django 4.2 on 2024-05-02 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields
import utils.uuid_generator


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0042_roadfund'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0014_delete_acceleratorfund'),
        ('quiz', '0013_alter_taskorder_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreRegisterTaskResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('file', models.FileField(blank=True, help_text='در صورت نیاز میتوانید یک فایل نیز برای شتابدهنده ارسال کنید', null=True, upload_to='task-response/%Y/%m/', verbose_name='فایل')),
                ('title', models.CharField(max_length=64, verbose_name='عنوان پاسخ')),
                ('text', django_quill.fields.QuillField(default='', verbose_name='محتوا متنی')),
                ('status', models.CharField(choices=[('w', 'در انتظار برسی'), ('d', 'تایید شده'), ('r', 'رد شده')], default='w', max_length=1, verbose_name='وضعیت')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ساخت')),
                ('last_update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='زمان بروزرسانی')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='road_of_pre_register_task_response', to='content.road', verbose_name='مسیر')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_of_pre_register_task_response', to='quiz.task', verbose_name='تسک')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_of_pre_register_task_response', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ کاربر به آزمون',
                'verbose_name_plural': 'پاسخ های کاربر به آزمون',
            },
        ),
        migrations.CreateModel(
            name='PreRegisterTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=utils.uuid_generator.random_uuid, editable=False, max_length=5, unique=True)),
                ('title', models.CharField(max_length=64, verbose_name='عنوان')),
                ('text', django_quill.fields.QuillField(default='', verbose_name='محتوا متنی')),
                ('start_date', models.DateField(null=True, verbose_name='تاریخ شروع')),
                ('expiration_date', models.DateField(null=True, verbose_name='تاریخ پایان')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ساخت')),
                ('last_update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='زمان بروزرسانی')),
                ('accelerator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accelerator_of_pre_register_task', to='company.center', verbose_name='برگزارکننده')),
            ],
            options={
                'verbose_name': 'آزمون',
                'verbose_name_plural': 'آزمون ها',
            },
        ),
    ]
