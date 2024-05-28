from django.db import models
from utils.uuid_generator import random_uuid



class Topic(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    name = models.CharField(verbose_name="نام", max_length=50)
    
    created_by = models.ForeignKey("account.User", verbose_name="سازنده", related_name="user_of_topic", on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "موضوع"
        verbose_name_plural = "موضوعات"

    def __str__(self) -> str:
        return self.name


class Subject(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )
    topic = models.ForeignKey(Topic, verbose_name="موضوع", related_name="topic_of_subject", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name="نام", max_length=50)
    
    created_by = models.ForeignKey("account.User", verbose_name="سازنده", related_name="user_of_subject", on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    last_update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "زیر موضوع"
        verbose_name_plural = "زیر موضوعات"

    def __str__(self) -> str:
        try:
            res = f"{self.name} [{self.topic.name}]"
        except:
            res = f"{self.name} [Null]"

        return res
