from django.db import models
from utils.uuid_generator import random_uuid


class NotifyLog(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    status = models.CharField(verbose_name="کد وضعیت", max_length=3)
    message = models.JSONField(verbose_name="پاسخ سرور", null=True)
    
    send_try = models.PositiveIntegerField(verbose_name="تلاش برای ارسال")
    
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")
    
    def __str__(self):
        return self.uuid
