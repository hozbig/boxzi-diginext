# Generated by Django 4.2 on 2024-06-25 15:35

from django.db import migrations, models
import utils.uuid_generator


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_preregistertaskresponse_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='examorder',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='personaltest',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='preregistertask',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='preregistertaskquestion',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='preregistertaskresponse',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='taskorder',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='taskresponse',
            name='uuid',
            field=models.CharField(blank=True, default=utils.uuid_generator.random_uuid4, editable=False, max_length=36, unique=True),
        ),
    ]
