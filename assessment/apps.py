from django.apps import AppConfig


class AssessmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assessment'
    verbose_name = "ارزیابی"

    # def ready(self):
    #     self.create_default_data()

    # def create_default_data(self):
    #     from .models import Category
    #     # Define the data you want to ensure is present
    #     default_data = [
    #         {'name': 'ارزیابی بخش فنی ایده و محصول', 'key_name': "plan"},
    #         {'name': 'ارزیابی بخش کسب‌وکار', 'key_name': "business"},
    #         {'name': 'بررسی تیم/فرد کارآفرین', 'key_name': "team_individual"},
    #         {'name': 'ارزیابی مهارت‌های نرم کارآفرین', 'key_name': "personal"},
    #         {'name': 'ارزیابی مهارت‌های تخصصی کارآفرین', 'key_name': "challenge"},
    #     ]

    #     for data in default_data:
    #         obj, created = Category.objects.get_or_create(name=data['name'], key_name=data['key_name'])
    #         if created:
    #             print(f"Created new entry: {obj}")
    #         else:
    #             print(f"Entry already exists: {obj}")
