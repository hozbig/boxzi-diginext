# Generated by Django 4.2 on 2024-04-21 08:37

from django.db import migrations, models
import team.models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0016_alter_teammember_user_number_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='user_number_id',
            field=models.CharField(default=0, max_length=10, validators=[team.models.validate_numeric], verbose_name='کد ملی فرد'),
        ),
    ]
