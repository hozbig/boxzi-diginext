# Generated by Django 4.2 on 2024-06-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_remove_teammember_temporary_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadregistration',
            name='complete_registration_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ تکمیل اطلاعات توسط کاربر'),
        ),
        migrations.AlterField(
            model_name='roadregistration',
            name='status_user_state',
            field=models.CharField(choices=[('0', 'درحال تکمیل ثبت نام'), ('1', 'ثبت اطلاعات اولیه'), ('2t', 'به عنوان تیم'), ('2i', 'به عنوان فرد'), ('f', 'ثبت نام کامل')], default='۱', max_length=2, verbose_name='وضعیت ثبت نام کاربر'),
        ),
    ]