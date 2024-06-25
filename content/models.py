import re
import readtime

from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from utils.uuid_generator import random_uuid


# content -> steps that are defined in roadmap
class Content(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    title = models.CharField(verbose_name="عنوان", max_length=255)
    video_link = models.URLField(verbose_name="لینک ویدیو", max_length=200, null=True, blank=True, help_text="آپارات یا یوتیوب")
    description = models.TextField(verbose_name="توضیح کوتاه", null=True, blank=True)
    content = QuillField(default="", verbose_name="محتوا متنی")
    subjects = models.ManyToManyField("subject.Subject", verbose_name="موضوعات مربوط")
    medals = models.PositiveIntegerField(verbose_name="مدال", default=0)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_content", verbose_name="مرکز شتابدهنده (ایجاد کننده محتوا)", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "محتوا"
        verbose_name_plural = "محتوا ها"

    def __str__(self) -> str:
        return self.title
    
    def get_aparat_code(self):
        """
        Extracts the unique code associated with the video from the input URL and returns it as output.
        """
        pattern = r'/([^/]+)/?$'
        try:
            match = re.search(pattern, self.video_link)
        except:
            return None
        if match:
            return match.group(1)
        else:
            return None
        
    def get_read_time(self):
        """
        Returns the number of minutes required to read the text.
        """
        result = readtime.of_text(self.content)
        return result.text.replace("min", "")
        

class WatchedContent(models.Model):
    user = models.ForeignKey("account.User", verbose_name="کاربر", related_name="user_of_watched_content", on_delete=models.CASCADE)
    content = models.ForeignKey(Content, verbose_name="محتوا", related_name="content_of_watched_content", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "گام طی شده"
        verbose_name_plural = "گام های طی شده"

    def __str__(self) -> str:
        return self.content.uuid


# Collections are SEASONS int he roadmap
class Collection(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    name = models.CharField(verbose_name="نام", max_length=50)
    subjects = models.ManyToManyField("subject.Subject", verbose_name="موضوعات")
    exam = models.ForeignKey("quiz.Exam", verbose_name="آزمون", related_name="exam_of_collection", on_delete=models.CASCADE, null=True, blank=True)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_collection", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)

    TYPES = (
        ("c", "کنجکاو"), # Curious
        ("e", "کارآفرین"), # Entrepreneur
        ("g", "عمومی"), # General
    )
    type = models.CharField(choices=TYPES, default="c", max_length=1, verbose_name="برای کاربران با نوع")

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "فصل آموزشی"
        verbose_name_plural = "فصل های"

    def __str__(self) -> str:
        return self.name


# order of steps that are defined in the acceleration program roadmap()
class ContentOrder(models.Model):
    collection = models.ForeignKey(Collection, verbose_name="فصل", on_delete=models.CASCADE, related_name="collection_of_content_order")
    content = models.ForeignKey(Content, verbose_name="محتوا", on_delete=models.CASCADE, related_name="content_of_content_order")
    row_number = models.PositiveIntegerField(verbose_name="شماره ردیف")

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ترتیب دوره"
        verbose_name_plural = "ترتیب دوره ها"
        ordering = ['row_number']

    def __str__(self) -> str:
        return f"{self.collection} - {self.content} - {self.row_number}"


# acceleration program (roadmap)
class Road(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    poster = models.ImageField(verbose_name="پوستر", upload_to="roads-poster/", null=True)
    name = models.CharField(verbose_name="نام مسیر", max_length=255)
    location = models.CharField(verbose_name="مکان برگزاری", max_length=255, null=True)

    HOLDING_METHODS = (
        ("s","حضوری"), # on Site
        ("o","آنلاین"), # Online
        ("h","حضوری و آنلاین"), # Hybrid
    )
    holding_method = models.CharField(verbose_name="شیوه برگزاری", max_length=1, default="h", choices=HOLDING_METHODS)
    price = models.PositiveIntegerField(verbose_name="هزینه ثبت نام", default=0)
    description = models.CharField(verbose_name="توضیحات کوتاه", max_length=255, null=True)
    start_date = models.DateField("تاریخ شروع", auto_now=False, auto_now_add=False, null=True)
    expiration_date = models.DateField("تاریخ پایان", auto_now=False, auto_now_add=False, null=True)
    publish_date = models.DateField("تاریخ انتشار", auto_now=False, auto_now_add=False, null=True)
    registration_deadline = models.DateField("مهلت ثبت نام", auto_now=False, auto_now_add=False, null=True)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_road", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)
    holders = models.ManyToManyField("company.Center", verbose_name="برگزارکنندگان", related_name="holders_of_road",)
    sponsors = models.ManyToManyField("company.Center", verbose_name="حمایت کنندگان", related_name="sponsors_of_road", blank=True)
    pre_register_task = models.ForeignKey("quiz.PreRegisterTask", related_name="pre_register_task_of_road", verbose_name="آزمون ورودی برای افراد توسعه دهنده تکنولوژی", null=True, on_delete=models.CASCADE)
    pre_register_task_for_business_side = models.ForeignKey("quiz.PreRegisterTask", related_name="pre_register_task_for_business_side_of_road", verbose_name="آزمون ورودی برای افراد توسعه دهنده کسب و کار", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "مسیر"
        verbose_name_plural = "مسیر ها"

    def __str__(self) -> str:
        return f"مسیر {self.name} - برگزارکننده {self.accelerator}"
    
    def save(self) -> None:
        super().save()
        try:
            fund = RoadFund.objects.create(road=self)
            fund.save()
        except:
            pass

    def days_until_expiration(self):
        try:
            today = timezone.now().date()
            days_until = (self.expiration_date - today).days
            return max(0, days_until + 1)
        except:
            return 0
    
    def days_until_start(self):
        try:
            today = timezone.now().date()
            days_until = (self.start_date - today).days
            return max(0, days_until + 1)
        except:
            return 0
    
    def days_until_publish(self):
        try:
            today = timezone.now().date()
            days_until = (self.publish_date - today).days
            return max(0, days_until + 1)
        except:
            return 0
    
    def days_until_registration_deadline(self):
        try:
            today = timezone.now().date()
            days_until = (self.registration_deadline - today).days
            return max(0, days_until + 1)
        except:
            return 0


class CollectionOrder(models.Model):
    road = models.ForeignKey(Road, verbose_name="مسیر", on_delete=models.CASCADE, related_name="road_of_collection_order", null=True)
    collection = models.ForeignKey(Collection, verbose_name="فصل", on_delete=models.CASCADE, related_name="collection_of_collection_order")
    row_number = models.PositiveIntegerField(verbose_name="شماره ردیف")

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ترتیب فصل"
        verbose_name_plural = "ترتیب فصل ها"
        ordering = ['row_number']

    def __str__(self) -> str:
        return f"{self.road} - {self.collection} - {self.row_number}"
    

class RoadFund(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    road = models.OneToOneField(Road, related_name="fund_of_road", verbose_name="برنامه", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کیف پول برنامه"
        verbose_name_plural = "کیف پول برنامه ها"

    def __str__(self) -> str:
        return f"کیف پول برنامه «{self.road.name}» از شتابدهنده {self.road.accelerator.name}"
