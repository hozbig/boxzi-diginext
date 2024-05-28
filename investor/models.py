from django.core.exceptions import ValidationError
from django.db import models
from utils.uuid_generator import random_uuid
from account.models import User

def validate_is_investor(value):
    value = User.objects.get(id=value)
    if not value.is_investor:
        raise ValidationError('کاربر انتخابی باید درسترسی سرمایه گذار را داشته باشد.')


class InvestorFound(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    investor = models.ForeignKey("account.User", verbose_name="سرمایه گذار", on_delete=models.CASCADE, validators=[validate_is_investor], related_name="fund_of_investor")
    name = models.CharField(verbose_name="نام صندوق", max_length=255)
    amount = models.PositiveIntegerField(default=0, verbose_name="حجم صندوق")

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد", null=True)
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی", null=True)

    class Meta:
        verbose_name = "صندوق"
        verbose_name_plural = "صندوق ها"

    def __str__(self) -> str:
        return self.name