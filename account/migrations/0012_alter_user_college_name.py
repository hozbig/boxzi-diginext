# Generated by Django 4.2 on 2024-06-08 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_user_programming_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='college_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='محل تحصیل'),
        ),
    ]