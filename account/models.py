from django.contrib.auth.models import AbstractUser
from django.db import models

from content.models import WatchedContent
from team.models import StartUpTeam
from utils.uuid_generator import random_uuid
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError(
            _('Value %(value)s is not numeric.'),
            params={'value': value},
        )


class User(AbstractUser):
    number_id = models.CharField(unique=True, null=True, blank=True, max_length=10, validators=[validate_numeric], verbose_name="کدملی")
    phone_number = models.CharField(verbose_name="شماره تماس", unique=True, max_length=11)
    birthday = models.DateField(verbose_name="تاریخ تولد", auto_now=False, auto_now_add=False, null=True, blank=True)

    
    is_mentor = models.BooleanField(verbose_name="مربی", default=False)
    is_team_member = models.BooleanField(verbose_name="عضو تیم", default=False)
    is_investor = models.BooleanField(verbose_name="سرمایه گذار", default=False)
    access_to_company = models.ManyToManyField("company.Company", verbose_name="دسترسی به شرکت", blank=True)
    
    access_to_center = models.ForeignKey("company.Center", verbose_name="دسترسی به مرکز", blank=True, null=True, on_delete=models.CASCADE)
    TYPES = (
        ("c", "کنجکاو"), # Curious
        ("e", "کارآفرین"), # Entrepreneur
    )
    type = models.CharField(choices=TYPES, max_length=1, verbose_name="نوع کاربر", null=True, blank=True)


    major = models.CharField(verbose_name="رشته تحصیلی", max_length=50, null=True, blank=True)
    interests = models.ManyToManyField("subject.Subject", verbose_name="علاقه مندی ها", related_name="interests_of_user", blank=True)
    abilities = models.ManyToManyField("subject.Subject", verbose_name="توانایی ها", related_name="abilities_of_user", blank=True)
    received_medals = models.PositiveIntegerField(default=0)
    bio = models.TextField(default="", verbose_name="بیوگرافی", blank=True, null=True)
    personal_website = models.URLField(verbose_name="وبسایت شخصی", max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'  # Set phone_number as the unique identifier
    REQUIRED_FIELDS = []  # Remove the required username field

    def is_profile_complete(self):
        if self.is_team_member or self.is_mentor:
            if self.first_name and self.last_name and self.email and self.birthday and self.major and self.bio:
                return self.interests.exists() and self.abilities.exists()
                return self.user_of_work_experience.exists() and self.interests.exists() and self.abilities.exists()
            else:
                return False
        elif self.is_company_staff() or self.is_center_staff() or self.is_staff or self.is_superuser:
            return self.first_name and self.last_name and self.email and self.birthday
        return False
    
    def is_profile_complete_level2(self):
        if self.first_name and self.last_name and self.email and self.phone_number and self.number_id and self.birthday:
            return True
            # return self.skills.exists()
        return False

    def get_active_collection(self):
        watched_contents = WatchedContent.objects.filter(user=self).reverse()
        for collection in self.collections.all():
            count_of_content = collection.contents.all().count()
            for content in collection.contents.all():
                if content in watched_contents:
                    count_of_content -= 1
                
                if count_of_content > 0:
                    return collection

    def is_company_staff(self):
        return self.access_to_company.exists()
    is_company_staff.boolean = True
    is_company_staff.short_description = "دسترسی به شرکت"

    def is_center_staff(self):
        if self.access_to_center is not None:
            return True
        else:
            return False
    is_center_staff.boolean = True
    is_center_staff.short_description = "دسترسی به مرکز"

    def add_medals(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Invalid medal value. Please provide a positive integer.")
        self.received_medals = (self.received_medals or 0) + value
        self.save()

    def get_total_team_member_count_for_mentor(mentor):
        # Get all teams related to the mentor
        related_teams = StartUpTeam.objects.filter(team_mentors=mentor)

        # Calculate the total team member count
        total_team_member_count = sum(team.team_member_count() for team in related_teams)

        return total_team_member_count
    
    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.phone_number


class Meeting(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    team = models.ForeignKey("team.StartUpTeam", verbose_name="تیم", related_name="team_of_meeting", null=True, on_delete=models.CASCADE)
    team_member = models.ForeignKey(User, verbose_name="عضو تیم", related_name="team_member_of_meeting", on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, verbose_name="مربی", related_name="mentor_of_meeting", on_delete=models.CASCADE)

    date = models.DateField("تاریخ", auto_now=False, auto_now_add=False)
    time = models.TimeField("ساعت", auto_now=False, auto_now_add=False)
    topic = models.CharField(verbose_name="موضوع", max_length=255)
    description = models.TextField(verbose_name="توضیحات")

    STATUS = (
        ("w", "در انتظار برسی مربی"), # Waiting
        ("a", "فعال"), # Active
        ("d", "انجام شده"), # Done
        ("c", "کنسل توسط کاربر"), # Cancell
        ("r", "ردشدن توسط مربی"), # Reject
    )
    status = models.CharField(choices=STATUS, max_length=1, default="w", verbose_name="وضعیت")

    rate = models.PositiveIntegerField(
        verbose_name="نمره",
        null=True,
        blank=True,
        validators=[MaxValueValidator(5)]
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسه ها"

    def __str__(self) -> str:
        return self.uuid


class WorkExperience(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    user = models.ForeignKey(User, verbose_name="کاربر", related_name="user_of_work_experience", on_delete=models.CASCADE)
    from_date = models.DateField("از تاریخ", auto_now=False, auto_now_add=False)
    to_date = models.DateField("تا تاریخ", auto_now=False, auto_now_add=False)
    topic = models.CharField(verbose_name="عنوان شغلی", max_length=255)
    description = models.TextField(verbose_name="توضیحات")

    TYPE = (
        ("f", "تمام وقت"), # Full-time
        ("p", "پاره وقت"), # Part-time
        ("j", "پروژه"), # proJect
    )
    type = models.CharField(choices=TYPE, max_length=1, default="f", verbose_name="نوع")

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "سابقه کاری"
        verbose_name_plural = "سابقه کاری ها"

    def __str__(self) -> str:
        return self.uuid


class LeanCanvas(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    data = models.JSONField(verbose_name="اطلاعات",)
    
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "بوم کسب و کار"
        verbose_name_plural = "بوم های کسب و کار"

    def __str__(self) -> str:
        return self.data
