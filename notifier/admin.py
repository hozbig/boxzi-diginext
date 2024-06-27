from django.contrib import admin
from .models import NotifyLog, OTP

class AdminNotifyLog(admin.ModelAdmin):
    list_display = ["status", "message", "action", "send_try",]
    
    list_filter = ["action", "status", "created_time"]


admin.site.register(NotifyLog, AdminNotifyLog)


class AdminOTP(admin.ModelAdmin):
    list_display = ["phone_number", "otp_code", "created_time",]
    
    list_filter = ["phone_number",]


admin.site.register(OTP, AdminOTP)