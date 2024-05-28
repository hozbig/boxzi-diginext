from django.db import models
from django.utils.html import mark_safe
from django_quill.fields import QuillField
from django.db.models import Count
from utils.uuid_generator import random_uuid
from plan.models import Plan
from account.models import User


class Company(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    name = models.CharField(verbose_name="اسم کسب و کار", max_length=255)
    domain = models.URLField(verbose_name="دامنه", max_length=255)
    logo = models.ImageField(verbose_name="لوگو", upload_to="company/logo/", null=True, blank=True)
    watching_subject = models.ManyToManyField("subject.Subject", verbose_name="موضوعات زیر نظر", related_name="watching_subject_of_company", blank=True)
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کسب و کار"
        verbose_name_plural = "کسب و کار ها"

    def __str__(self) -> str:
        return self.name
    
    def logo_preview(self) -> str:
        if self.logo:
            return mark_safe('<img src="{}" width="100px" />'.format(self.logo.url))
        return ""

    logo_preview.short_description = "پیشنمایش عکس"


class Product(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    company = models.ForeignKey(Company, verbose_name="کمپانی", related_name="product_of_company", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="نام خدمت یا محصول", max_length=255)
    price = models.PositiveIntegerField(verbose_name="مدال مورد نیاز", default=0)
    description = models.TextField(verbose_name="توضیحات")

    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "خدمت یا کالا"
        verbose_name_plural = "خدمت ها یا کالا ها"
        ordering = ["-created_time"]

    def __str__(self) -> str:
        return f"{self.name} > {self.company.name}"
    
    
class Center(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    name = models.CharField(verbose_name="اسم مرکز", max_length=255)
    short_description = models.TextField(default="", verbose_name="توضیحات کوتاه")
    domain = models.URLField(verbose_name="دامنه", max_length=255, null=True, blank=True)
    logo = models.ImageField(verbose_name="لوگو", upload_to="company/logo/", null=True, blank=True)
    state = models.CharField(verbose_name="استان", max_length=255)
    
    TYPES = (
        ("g", "مرکز رشد"), # Growth center
        ("a", "مرکز شتابدهی"), # Acceleration center
        ("i", "کارخونه نوآوری"), # Innovation factory
    )
    type = models.CharField(verbose_name="نوع", max_length=1, choices=TYPES)
    activity = models.CharField(verbose_name="حوزه فعالیت", max_length=255)
    teams = models.ManyToManyField("team.StartUpTeam", verbose_name="تیم های استارتاپی", blank=True, related_name="team_of_center")
    mentors = models.ManyToManyField("account.User", verbose_name="مربی ها", blank=True)

    description = QuillField(default="", verbose_name="توضیحات", blank=True)
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مرکز"
        verbose_name_plural = "مراکز"

    def __str__(self) -> str:
        return self.name
        
    def count_team_members(self):
        # Get all the users related to teams associated with the center
        team_members_count = User.objects.filter(
            members_of_team__in=self.teams.all()
        ).distinct().count()
        return team_members_count
    
    def count_team_plans(self):
        return Plan.objects.filter(team__in=self.teams.all()).count()
    
    def logo_preview(self) -> str:
        if self.logo:
            return mark_safe('<img src="{}" width="100px" />'.format(self.logo.url))
        return ""

    logo_preview.short_description = "پیشنمایش عکس"
