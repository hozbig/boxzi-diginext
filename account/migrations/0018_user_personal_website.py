# Generated by Django 4.2 on 2024-03-10 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_alter_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='personal_website',
            field=models.URLField(blank=True, null=True, verbose_name='وبسایت شخصی'),
        ),
    ]
