from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from team.models import StartUpTeam
from django_quill.fields import QuillField
from utils.uuid_generator import random_uuid


def validate_is_investor(value):
    if not value.is_investor or not value.access_to_center():
        raise ValidationError('کاربر انتخابی باید درسترسی سرمایه گذار یا ادمین شتابدهنده را داشته باشد.')


class Plan(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    user = models.ForeignKey("account.User", verbose_name="کاربر", related_name="user_of_plan", null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(StartUpTeam, verbose_name="تیم", related_name="team_of_plan", null=True, blank=True, on_delete=models.CASCADE)
    logo = models.ImageField(verbose_name="لوگو", upload_to="plan/logo/", null=True, blank=True)
    name = models.CharField(verbose_name="نام محصول", max_length=255)
    industry = models.CharField(verbose_name="صنعت", max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name="توصیف کوتاه")
    text = QuillField(verbose_name="توضیحات کامل", default="", null=True, blank=True)
    has_mvp = models.BooleanField(verbose_name="دارای کمینه", null=True, blank=True)
    likes = models.ManyToManyField("account.User", related_name='user_of_likes_plan', blank=True)
    
    STATUS = (
        ("p", "درحال انجام"), # inProgress
        ("f", "تمام شده"), # Finish
    )
    status = models.CharField(choices=STATUS, max_length=1, default="p", verbose_name="وضعیت", null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "محصول یا ایده"
        verbose_name_plural = "محصول ها و ایده ها"

    def __str__(self) -> str:
        return self.name
    
    def logo_preview(self) -> str:
        if self.logo:
            return mark_safe('<img src="{}" width="100px" />'.format(self.logo.url))
        return ""

    logo_preview.short_description = "پیشنمایش عکس"

    def likes_count(self):
        return self.likes.count()


class ProductWallet(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    product = models.OneToOneField(Plan, related_name="wallet_of_product", verbose_name="محصول", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "کیف پول محصول"
        verbose_name_plural = "کیف پول محصول ها"

    def __str__(self) -> str:
        if self.product.team:
            return f"کیف پول محصول «{self.product.name}» از تیم {self.product.team.name}"
        return f"کیف پول محصول «{self.product.name}» از {self.product.user.get_full_name()}"
