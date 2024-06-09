from django.contrib.auth.models import AbstractUser, BaseUserManager
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
        
def resume_directory_path(instance, filename):
    return f'users/resumes/{instance.uuid}/{filename}'

def why_us_directory_path(instance, filename):
    return f'users/why_us/{instance.uuid}/{filename}'


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    username = None
    phone_number = models.CharField(verbose_name="شماره تماس", unique=True, max_length=11, primary_key=True)
    number_id = models.CharField(unique=True, null=True, blank=True, max_length=10, validators=[validate_numeric], verbose_name="کدملی")
    birthday = models.DateField(verbose_name="تاریخ تولد", auto_now=False, auto_now_add=False, null=True, blank=True)

    is_mentor = models.BooleanField(verbose_name="مربی", default=False)
    is_team_member = models.BooleanField(verbose_name="عضو تیم", default=False)
    is_investor = models.BooleanField(verbose_name="سرمایه گذار", default=False)
    is_company = models.BooleanField(verbose_name="شرکت", default=False)
    
    access_to_center = models.ForeignKey("company.Center", verbose_name="دسترسی به مرکز", blank=True, null=True, on_delete=models.CASCADE)

    DEGREE = (
        ("d", "دیپلم"), # Diplome
        ("k", "کاردانی"), # Kardani
        ("l", "کارشناسی"), # Lisans
        ("f", "کارشناسی ارشد"), # Fogh lisans
        ("o", "دکترا"), # dOctora
    )
    degree = models.CharField(verbose_name="مقطع تحصیلی", max_length=1, choices=DEGREE, default="d")
    college_name = models.CharField(verbose_name="محل تحصیل", max_length=50, null=True, blank=True)
    province = models.CharField(verbose_name="استان محل سکونت", max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name="شهر محل سکونت", max_length=50, null=True, blank=True)
    interests = models.ManyToManyField("subject.Subject", verbose_name="علاقه مندی ها", related_name="interests_of_user", blank=True)
    abilities = models.ManyToManyField("subject.Subject", verbose_name="توانایی ها", related_name="abilities_of_user", blank=True)
    
    TYPES = (
        ("t", "فنی"), # Tech side
        ("b", "بیزنسی"), # Business side
    )
    type = models.CharField(choices=TYPES, max_length=1, verbose_name="نقش شما", default="t")
    resume_file = models.FileField(verbose_name="فایل pdf رزومه", upload_to=resume_directory_path, null=True, blank=True)
    
    YESNO = (
        ("y", "داشته ام"), # Yes
        ("n", "نداشته ام"), # No
    )
    is_accelerator_experience = models.CharField(choices=YESNO, max_length=1, verbose_name="تجربه شرکت در برنامه شتابدهی داشته اید؟", default="n")
    if_is_accelerator_experience = models.JSONField(verbose_name="اطلاعات مربوط به برنامه شتابدهی شرکت کرده توسط کابر", null=True, blank=True)
    
    STARTUP_EXPERIENCE = (
        ("m", "تجربه عضویت در استارت آپ دارم"), # Member
        ("c", "تجربه بنیانگذاری یک استارت اپ را دارم"), # Coordinator
        ("n", "هیچ تجربه ای ندارم"), # No experience
    )
    is_startup_experience = models.CharField(choices=STARTUP_EXPERIENCE, max_length=1, verbose_name="عضو یا بنیانگذار یک استارتاپ بوده اید؟", default="n")
    if_is_startup_experience = models.JSONField(verbose_name="اطلاعات مربوط به تجربه استارتاپی کابر", null=True, blank=True)

    programming_language = models.CharField(verbose_name="زبانه برنامه نویسی تخصصی شما", max_length=255, null=True, blank=True)
    specialty = models.CharField(verbose_name="زمینه تخصصی شما", max_length=255, null=True, blank=True)
    other_specialties = models.CharField(verbose_name="دیگر تخصص های شما", max_length=255, null=True, blank=True)
    why_us = models.TextField(default="", verbose_name="علت درخواست شما برای برنامه شتابدهی", blank=True, null=True)
    why_us_video = models.FileField(verbose_name="توضیحات کوتاه شما به صورت فیلم", upload_to=why_us_directory_path, max_length=100, null=True, blank=True)

    bio = models.TextField(default="", verbose_name="بیوگرافی", blank=True, null=True)

    USERNAME_FIELD = 'phone_number'  # Set phone_number as the unique identifier
    REQUIRED_FIELDS = []  # Remove the required username field
    
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def is_profile_complete(self):
        if self.is_team_member or self.is_mentor:
            if self.first_name and self.last_name and self.email and self.birthday and self.degree and self.college_name and self.province and self.city and self.type and self.is_accelerator_experience and self.is_startup_experience and self.specialty and self.why_us:
                return True
                # return self.user_of_work_experience.exists() and self.interests.exists() and self.abilities.exists()
            else:
                return False
        elif self.is_company_staff() or self.is_center_staff() or self.is_staff or self.is_superuser:
            return self.first_name and self.last_name and self.email and self.birthday
        return False
    
    def is_profile_complete_level2(self):
        if self.is_profile_complete() and self.number_id and self.bio:
            return self.interests.exists() and self.abilities.exists()
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

    def is_center_staff(self):
        if self.access_to_center is not None:
            return True
        else:
            return False
    is_center_staff.boolean = True
    is_center_staff.short_description = "دسترسی به مرکز"

    def get_total_team_member_count_for_mentor(mentor):
        # Get all teams related to the mentor
        related_teams = StartUpTeam.objects.filter(team_mentors=mentor)

        # Calculate the total team member count
        total_team_member_count = sum(team.team_member_count() for team in related_teams)

        return total_team_member_count


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
