# Generated by Django 4.2 on 2024-06-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_alter_preregistertaskresponse_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preregistertask',
            name='type',
            field=models.CharField(choices=[('t', 'تکنولوژی'), ('b', 'کسب\u200cوکار')], default='t', max_length=1, verbose_name='نوع'),
        ),
    ]