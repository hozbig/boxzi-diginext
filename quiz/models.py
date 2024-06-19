from django.db import models
from utils.uuid_generator import random_uuid
from django_quill.fields import QuillField


class Answer(models.Model):
    text = models.CharField(max_length=128, verbose_name="متن")
    is_valid = models.BooleanField(default=False, verbose_name="درست بودن")
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_answer", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "جواب"
        verbose_name_plural = "جواب ها"

    def __str__(self) -> str:
        return f"{self.text} : {self.is_valid}"


class Question(models.Model):
    text = models.CharField(max_length=256, verbose_name="متن")
    answers = models.ManyToManyField(Answer, verbose_name="گزینه ها", blank=True)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_question", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "سوآل"
        verbose_name_plural = "سوآل ها"

    def __str__(self) -> str:
        return self.text


class Exam(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    name = models.CharField(max_length=64, verbose_name="عنوان")
    questions = models.ManyToManyField(Question, verbose_name="سوال ها", blank=True)
    medals = models.PositiveIntegerField(verbose_name="مدال", default=0)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_exam", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون ها"

    def __str__(self) -> str:
        return self.name


class UserExamAnsewrHistory(models.Model):
    user = models.ForeignKey("account.user", related_name="ansewr_history_of_user", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name="ansewr_history_of_exam", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="ansewr_history_of_question", on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name="ansewr_history_of_answer", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "پاسخ ها کاربر"
        verbose_name_plural = "پاسخ های کاربر "

    def __str__(self):
        return f"{self.user} - {self.exam} - {self.question} - {self.answer}"


class ExamOrder(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    collection = models.ForeignKey("content.collection", verbose_name="فصل", on_delete=models.CASCADE, related_name="collection_of_exam_order", null=True)
    exam = models.ForeignKey(Exam, verbose_name="آزمون", on_delete=models.CASCADE, related_name="road_of_exam_order", null=True)
    row_number = models.PositiveIntegerField(verbose_name="شماره ردیف")

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "ترتیب آزمون"
        verbose_name_plural = "ترتیب آزمون ها"

    def __str__(self) -> str:
        return f"{self.collection} - {self.exam} - {self.row_number}"
    
    
class Task(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    title = models.CharField(max_length=64, verbose_name="عنوان")
    text = QuillField(default="", verbose_name="محتوا متنی")
    medals = models.PositiveIntegerField(verbose_name="مدال", default=0)
    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_task", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "تسک"
        verbose_name_plural = "تسک ها"

    def __str__(self) -> str:
        return self.title


class TaskOrder(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    collection = models.ForeignKey("content.collection", verbose_name="فصل", on_delete=models.CASCADE, related_name="collection_of_task_order", null=True)
    task = models.ForeignKey(Task, verbose_name="تسک", on_delete=models.CASCADE, related_name="road_of_task_order", null=True)
    row_number = models.PositiveIntegerField(verbose_name="شماره ردیف")

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "ترتیب تسک"
        verbose_name_plural = "ترتیب تسک ها"

    def __str__(self) -> str:
        return f"{self.collection.name} : {self.task.title} - {self.row_number}"


class TaskResponse(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    user = models.ForeignKey("account.User", verbose_name="کاربر", related_name="user_of_task_response", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name="تسک", related_name="task_of_task_response", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="فایل", upload_to="task-response/%Y/%m/", max_length=100)
    title = models.CharField(max_length=64, verbose_name="عنوان")
    text = QuillField(default="", verbose_name="محتوا متنی")
    
    STATUS = (
        ("w", "در انتظار برسی"), # Waiting
        ("d", "تایید شده"), # Done
        ("r", "رد شده"), # Reject
    )
    status = models.CharField(choices=STATUS, max_length=1, default="w", verbose_name="وضعیت")

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "پاسخ تسک"
        verbose_name_plural = "پاسخ تسک ها"

    def __str__(self) -> str:
        return self.title


class PreRegisterTask(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    title = models.CharField(max_length=64, verbose_name="عنوان")
    text = QuillField(default="", verbose_name="محتوا متنی")
    start_date = models.DateField("تاریخ شروع", auto_now=False, auto_now_add=False, null=True)
    expiration_date = models.DateField("تاریخ پایان", auto_now=False, auto_now_add=False, null=True)
    TYPES = (
        ("t", "فنی"), # Tech
        ("b", "بیزنسی"), # Business
    )
    type = models.CharField(choices=TYPES, max_length=1, default="t", verbose_name="نوع")

    accelerator = models.ForeignKey("company.Center", related_name="accelerator_of_pre_register_task", verbose_name="برگزارکننده", null=True, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "آزمون پیش ثبت نام"
        verbose_name_plural = "آزمون های پیش ثبت نام"

    def __str__(self) -> str:
        return f"{self.title} ({self.get_type_display()})"


class PreRegisterTaskResponse(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    # The user who answered to pre register task
    user = models.ForeignKey("account.User", verbose_name="کاربر", related_name="user_of_pre_register_task_response", on_delete=models.CASCADE)
    # The task that user answered
    task = models.ForeignKey(PreRegisterTask, verbose_name="تسک", related_name="task_of_pre_register_task_response", on_delete=models.CASCADE)
    # The road that user want to sign for
    road = models.ForeignKey("content.Road", verbose_name="مسیر", related_name="road_of_pre_register_task_response", on_delete=models.CASCADE)
    
    file = models.FileField(verbose_name="فایل", upload_to="task-response/%Y/%m/", max_length=100, null=True, blank=True, help_text="در صورت نیاز میتوانید یک فایل نیز برای شتابدهنده ارسال کنید")
    title = models.CharField(max_length=64, verbose_name="عنوان پاسخ")
    text = QuillField(default="", verbose_name="محتوا متنی")
    
    STATUS = (
        ("w", "در انتظار برسی"), # Waiting
        ("d", "تایید شده"), # Done
        ("r", "رد شده"), # Reject
    )
    status = models.CharField(choices=STATUS, max_length=1, default="w", verbose_name="وضعیت")

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "پاسخ کاربر به آزمون"
        verbose_name_plural = "پاسخ های کاربر به آزمون"

    def __str__(self) -> str:
        return self.title


class PersonalTest(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    user = models.ForeignKey("account.User", verbose_name="کاربر", related_name="user_of_personal_test", on_delete=models.CASCADE)
    road = models.ForeignKey("content.Road", verbose_name="مسیر", related_name="road_of_personal_test", on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "چالش مهارت نرم"
        verbose_name_plural = "آزمون های شخصیت"

    def __str__(self) -> str:
        return f"{self.user} - {self.road.name}"
