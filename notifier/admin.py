from django.contrib import admin
from .models import NotifyLog

class AdminNotifyLog(admin.ModelAdmin):
    list_display = ["status", "message", "action", "send_try",]
    
    list_filter = ["action", "status", "created_time"]


admin.site.register(NotifyLog, AdminNotifyLog)