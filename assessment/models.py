from django.db import models
from utils.uuid_generator import random_uuid


class Category(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    name = models.CharField(verbose_name="نام", max_length=255)
    key_name = models.CharField(verbose_name="نام کلیدی", max_length=50)

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته بندی سوال"
        verbose_name_plural = "دسته بندی های سوال ها"

    def __str__(self) -> str:
        return self.name
    
    def count_of_questions(self) -> int:
        return self.category_of_question.all().count()
    
    
class Question(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    question = models.CharField(verbose_name="سوال", max_length=255)
    category = models.ForeignKey(Category, verbose_name="دسته بندی", on_delete=models.CASCADE, related_name="category_of_question")

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوال ها"

    def __str__(self) -> str:
        return self.question


class Response(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    
    question = models.ForeignKey(Question, verbose_name="سوال", on_delete=models.CASCADE, related_name="question_of_assessment_response")
    referee = models.ForeignKey("account.User", verbose_name="داور", on_delete=models.CASCADE, related_name="referee_of_assessment_response")
    point = models.PositiveIntegerField(verbose_name="امتیاز", default=0)
    
    plan = models.ForeignKey("plan.Plan", verbose_name="ایده / محصول", on_delete=models.CASCADE, null=True, blank=True, related_name="plan_of_assessment_response")
    team = models.ForeignKey("team.StartUpTeam", verbose_name="تیم", on_delete=models.CASCADE, null=True, blank=True, related_name="team_of_assessment_response")
    individual = models.ForeignKey("account.User", verbose_name="فرد", on_delete=models.CASCADE, null=True, blank=True, related_name="individual_of_assessment_response")
    personal_test = models.ForeignKey("quiz.PersonalTest", verbose_name="مهارت نرم", on_delete=models.CASCADE, null=True, blank=True, related_name="personal_test_of_assessment_response")
    pre_register_change = models.ForeignKey("quiz.PreRegisterTaskResponse", verbose_name="مهارت تخصصی", on_delete=models.CASCADE, null=True, blank=True, related_name="pre_register_change_of_assessment_response")

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پاسخ"
        verbose_name_plural = "پاسخ ها"

    def __str__(self) -> str:
        return self.question.question
