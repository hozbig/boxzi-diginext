# Generated by Django 4.2 on 2024-06-03 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_resume_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_startup_experience',
            field=models.CharField(choices=[('m', 'تجربه عضویت در استارت آپ دارم'), ('c', 'تجربه بنیانگذاری یک استارت اپ را دارم'), ('n', 'هیچ تجربه ای ندارم')], default='n', max_length=1, verbose_name='عضو یا بنیانگذار یک استارتاپ بوده اید؟'),
        ),
        migrations.AlterField(
            model_name='user',
            name='other_specialties',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='دیگر تخصص های شما'),
        ),
    ]