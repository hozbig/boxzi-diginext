from typing import Iterable
from django.db import models
from django.db.models import Q
from utils.uuid_generator import random_uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError(
            _('کدملی باید شامل اعداد باشد.'),
            params={'value': value},
        )


class Category(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    name = models.CharField(verbose_name="نام", max_length=255)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self) -> str:
        return self.name


class StartUpTeam(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    name = models.CharField(verbose_name="نام تیم", max_length=255)
    STATUS = (
        ("a", "فعال"), # Active
        ("i", "غیر فعال"), # Inactive
    )
    status = models.CharField(choices=STATUS, max_length=1, default="a", verbose_name="وضعیت", null=True, blank=True)
    description = models.TextField(verbose_name="بیوگرافی تیم")
    category = models.CharField(verbose_name="دسته بندی زمینه فعالیت", max_length=255)
    # TODO: team_members and team_mentors need to delete. our solutions for specify the members and mentors are changed.
    team_members = models.ManyToManyField("account.User", verbose_name="اعضای تیم", related_name="members_of_team", blank=True)
    team_mentors = models.ManyToManyField("account.User", verbose_name="مربی های تیم", related_name="mentors_of_team", blank=True)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "تیم"
        verbose_name_plural = "تیم ها"

    def __str__(self) -> str:
        return self.name
    
    def team_member_count(self) -> int:
        return self.team_of_team_member.count()
    team_member_count.short_description = "تعداد اعضا"
    
    
def search_items(query:str):
    qs = query.split(",")
    
    # Filter Category objects
    # categories = Category.objects.filter(
    #     Q(name__icontains=query)
    # )

    # Filter StartUpTeam objects
    result = None
    
    for q in qs:
        if result is None:
            result = StartUpTeam.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
        else:
            tmp = StartUpTeam.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
            result | tmp

    unique_result = result.distinct()

    return unique_result


class TeamMember(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    team = models.ForeignKey(StartUpTeam, verbose_name="تیم", on_delete=models.CASCADE, related_name="team_of_team_member")
    user = models.ForeignKey("account.User", verbose_name="عضو", on_delete=models.CASCADE, related_name="user_of_team_member", null=True, blank=True)
    is_coordinator = models.BooleanField(verbose_name="هماهنگ کننده؟", default=False)
    is_owner = models.BooleanField(verbose_name="سازنده این تیم؟", default=False)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "عضو های تیم"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} از تیم {self.team.name}"


class RoadRegistration(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    team = models.ForeignKey(StartUpTeam, related_name="team_of_road_registration", verbose_name="تیم", on_delete=models.CASCADE, null=True, blank=True)
    team_name = models.CharField(verbose_name="نام تیم", max_length=255, null=True, blank=True)
    user = models.ForeignKey("account.User", related_name="user_of_road_registration", verbose_name="کاربر", on_delete=models.CASCADE)
    road = models.ForeignKey("content.Road", related_name="road_of_road_registration", verbose_name="مسیر", on_delete=models.CASCADE)

    STATUS = (
        ("w", "عدم برسی شتابدهنده"), # Waiting
        ("p", "درحال برسی شتابدهنده"), # Progressing
        ("a", "تایید شده"), # Approved
        ("r", "رد شده"), # Reject
        ("c", "نیاز به اصلاح توسط شما"), # Correction
    )
    status = models.CharField(verbose_name="وضعیت", max_length=1, default="w", choices=STATUS)

    client_last_response_date = models.DateField("زمان آخرین تغییر توسط کاربر", auto_now=False, auto_now_add=False, null=True, blank=True)
    accelerator_last_response_date = models.DateField("زمان آخرین واکنش توسط شتابدهنده", auto_now=False, auto_now_add=False, null=True, blank=True)

    team_or_individual = models.CharField(verbose_name="تیم یا فرد؟", max_length=1, default="t", choices=(("t","تیم"),("i","فرد")))
    STATUS_USER_STATE = (
        ("0", "درحال تکمیل ثبت نام"),
        ("1", "تکمیل ثبت نام اولیه"),
        ("f", "ثبت نام کامل"),
    )
    status_user_state = models.CharField(verbose_name="وضعیت ثبت نام کاربر", max_length=2, default="۱", choices=STATUS_USER_STATE)

    complete_registration_date = models.DateField("تاریخ تکمیل اطلاعات توسط کاربر", auto_now=False, auto_now_add=False, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "ثبت نام مسیر آموزشی"
        verbose_name_plural = "ثبت نام مسیرهای آموزشی"

    def __str__(self) -> str:
        return f"{self.user} - {self.road}"
