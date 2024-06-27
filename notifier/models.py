from django.db import models
from datetime import timedelta
from django.utils import timezone
from utils.uuid_generator import random_uuid4
from account.models import User


class NotifyLog(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=36,
        blank=True,
        default=random_uuid4,
        editable=False,
    )
    
    status = models.CharField(verbose_name="کد وضعیت", max_length=255)
    message = models.TextField(verbose_name="پاسخ سرور", null=True)
    action = models.CharField(verbose_name="اسم عملیات", max_length=255, null=True, blank=True)
    
    send_try = models.PositiveIntegerField(verbose_name="تلاش برای ارسال")
    
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")
    
    def __str__(self):
        return self.uuid


class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    phone_number = models.CharField(verbose_name="شماره تماس", max_length=11)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    def is_valid(self):
        return self.created_time >= timezone.now() - timedelta(minutes=3)
