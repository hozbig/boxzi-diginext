from typing import Union
from django.db import models
from django.db.models import Q
from datetime import date
from utils.uuid_generator import random_uuid4
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
        max_length=36,
        blank=True,
        default=random_uuid4,
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
        max_length=36,
        blank=True,
        default=random_uuid4,
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
    
    def all_users_completed_registration(self) -> bool:
        team_member_objects = self.team_of_team_member.all()
        team_member_count = team_member_objects.count() - 1
        coordinator_completion_status = None

        if team_member_count < 1:
            return False

        for member in team_member_objects:
            member_register_object = member.user.user_of_road_registration.first()

            if member_register_object.team != self:
                continue

            if member.is_owner:
                coordinator_completion_status = member_register_object.is_complete_registration_for_coordinator()
                continue

            if member_register_object.is_complete_registration_for_team_member():
                team_member_count -= 1

        if team_member_count == 0:
            team_member_count = True
        else:
            team_member_count = False

        return team_member_count and coordinator_completion_status
    
    
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
        max_length=36,
        blank=True,
        default=random_uuid4,
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
        max_length=36,
        blank=True,
        default=random_uuid4,
        editable=False,
    )
    team = models.ForeignKey(StartUpTeam, related_name="team_of_road_registration", verbose_name="تیم", on_delete=models.CASCADE, null=True, blank=True)
    team_name = models.CharField(verbose_name="نام تیم", max_length=255, null=True, blank=True)
    user = models.ForeignKey("account.User", related_name="user_of_road_registration", verbose_name="کاربر", on_delete=models.CASCADE)
    road = models.ForeignKey("content.Road", related_name="road_of_road_registration", verbose_name="مسیر", on_delete=models.CASCADE)

    STATUS = (
        ("n", "شما نیاز به تکمیل فرایند ثبت‌نام خود دارید"), # Need to complete the profile
        ("w", "درخواست شما توسط برگزار کننده هنوز بررسی نشده است"), # Waiting
        ("p", "درخواست شما در حال بررسی توسط برگزارکننده می‌باشد"), # Progressing
        ("a", "پذیرش شما در برنامه تایید شده است"), # Approved
        ("r", "درخواست شما رد شده"), # Reject
        ("c", "شما برای تکمیل فرایند ثبت‌نام نیاز به اصلاح درخواست و اطلاعات خود دارید"), # Correction
    )
    status = models.CharField(verbose_name="وضعیت", max_length=1, default="n", choices=STATUS)

    client_last_response_date = models.DateField("زمان آخرین تغییر توسط کاربر", auto_now=False, auto_now_add=False, null=True, blank=True)
    accelerator_last_response_date = models.DateField("زمان آخرین واکنش توسط شتابدهنده", auto_now=False, auto_now_add=False, null=True, blank=True)

    TEAM_OR_INDIVIDUAL = (
        ("t", "تیم"),
        ("i", "فرد"),
        ("a", "تیم (اضافه شده توسط هماهنگ کننده)"),
    )
    team_or_individual = models.CharField(verbose_name="تیم یا فرد؟", max_length=1, default="t", choices=TEAM_OR_INDIVIDUAL)
    STATUS_USER_STATE = (
        ("2", "مرحله دوم تکمیل ثبت نام"),
        ("3", "مرحله سوم تکمیل ثبت نام"),
        ("4", "مرحله چهارم تکمیل ثبت نام"),
        ("5", "ثبت نام کامل"),
    )
    status_user_state = models.CharField(verbose_name="وضعیت ثبت نام کاربر", max_length=2, default="۱", choices=STATUS_USER_STATE)

    # validity_pride_days = validity_period_days
    # for all process in user request
    validity_pride_days = models.PositiveIntegerField(verbose_name="مهلت تکمیل درخواست (به روز)", default=10)
    # for complete the challenge
    validity_pride_days_for_challenge = models.PositiveIntegerField(verbose_name="مهلت تکمیل چالش (به روز)", default=3)
    complete_registration_date = models.DateField("تاریخ تکمیل اطلاعات توسط کاربر", auto_now=False, auto_now_add=False, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین بروزرسانی")

    class Meta:
        verbose_name = "ثبت نام مسیر آموزشی"
        verbose_name_plural = "ثبت نام مسیرهای آموزشی"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - مسیر {self.road.name}"
    
    def is_valid_registration_period(self):
        """_summary_

        Returns:
            False (boolean): It will be returned if the user registration is not complete.
            'True' (string): It mean user complete the registration.
            __int__ : It show the days passed from the registration date. This is obtained by subtracting the user's registration completion date from today's date.
        """
        
        try: # If registration for a team
            team_owner = self.team.team_of_team_member.filter(is_owner=True).first().user
            
            if team_owner.user_of_road_registration.first().client_last_response_date:
                return "True"
            
            team_owner_complete_registration_date = team_owner.user_of_road_registration.first().complete_registration_date
            team_owner_validity_pride_days = team_owner.user_of_road_registration.first().validity_pride_days

            if team_owner_complete_registration_date is None:
                return False 

            days_passed = (date.today() - team_owner_complete_registration_date).days
            return team_owner_validity_pride_days - days_passed
        except: # If registration for an individual
            if self.client_last_response_date:
                return "True"
            
            if self.complete_registration_date is None:
                return False  # or True depending on your requirement when there's no start date

            days_passed = (date.today() - self.complete_registration_date).days
            return self.validity_pride_days - days_passed
        
    def is_valid_registration_period_for_challenge(self):
        """_summary_

        Returns:
            False (boolean): It will be returned if the user registration is not complete.
            'True' (string): It mean user complete the registration.
            __int__ : It show the days passed from the registration date. This is obtained by subtracting the user's registration completion date from today's date.
        """
        
        if self.client_last_response_date:
            return "True"
        
        if self.complete_registration_date is None:
            return False  # or True depending on your requirement when there's no start date

        days_passed = (date.today() - self.complete_registration_date).days
        return self.validity_pride_days_for_challenge - days_passed

    def days_to_complete_registration(self):
        try: # If registration for a team
            team_owner = self.team.team_of_team_member.filter(is_owner=True).first().user
            team_owner_complete_registration_date = team_owner.user_of_road_registration.first().complete_registration_date
            # team_owner_validity_pride_days = team_owner.user_of_road_registration.first().validity_pride_days

            if team_owner_complete_registration_date is None:
                return False 

            days_passed = (date.today() - team_owner_complete_registration_date).days
            return days_passed
        except: # If registration for an individual
            if self.complete_registration_date is None:
                return False  # or True depending on your requirement when there's no start date

            days_passed = (date.today() - self.complete_registration_date).days
            return days_passed

    def is_complete_registration_for_coordinator(self) -> Union[bool, None]:
        if self.team_or_individual == "t":
            user = self.user
            is_profile_complete = user.is_profile_complete()

            if user.user_of_personal_test.exists() and not user.user_of_personal_test.first().final_user_result_url == None:
                has_personal_test = True
            else:
                has_personal_test = False
            
            first_team_member = user.user_of_team_member.first()
            if not first_team_member:
                return False
            
            team = first_team_member.team
            team_member_count = team.team_member_count() > 1
            has_team_plan = team.team_of_plan.exists()
            
            return is_profile_complete and has_personal_test and team_member_count and has_team_plan
            
        return None

    def is_complete_registration_for_team_member(self) -> Union[bool, None]:
        if self.team_or_individual == "a":
            user = self.user
            is_profile_complete = user.is_profile_complete()

            if user.user_of_personal_test.exists() and not user.user_of_personal_test.first().final_user_result_url == None:
                has_personal_test = True
            else:
                has_personal_test = False
            
            return is_profile_complete and has_personal_test
            
        return None
    
    def is_complete_registration_for_individual(self) -> Union[bool, None]:
        if self.team_or_individual == "i":
            user = self.user
            is_profile_complete = user.is_profile_complete()

            if user.user_of_personal_test.exists() and not user.user_of_personal_test.first().final_user_result_url == None:
                has_personal_test = True
            else:
                has_personal_test = False

            task_business_side = self.road.pre_register_task_for_business_side
            task = self.road.pre_register_task

            count_of_t_question = task.pre_register_of_pre_register_task_question.count()
            count_of_b_question = task_business_side.pre_register_of_pre_register_task_question.count()
            user_response_count = user.user_of_pre_register_task_response.count()

            if user.user_of_road_registration.first().team_or_individual == "i":
                if user.type == "t":
                    if (count_of_t_question - user_response_count) < 1:
                        has_challenge_response = True
                    else:
                        has_challenge_response = False
                elif user.type == "b":
                    if (count_of_b_question - user_response_count) < 1:
                        has_challenge_response = True
                    else:
                        has_challenge_response = False
            
            return is_profile_complete and has_personal_test and has_challenge_response
            
        return None

    def is_challenge_complete(self):
        user = self.user
        road = self.road
        task = road.pre_register_task
        task_business_side = road.pre_register_task_for_business_side

        count_of_questions = 0
        if user.type == "t":
            count_of_questions = task.pre_register_of_pre_register_task_question.count()
        elif user.type == "b":
            count_of_questions = task_business_side.pre_register_of_pre_register_task_question.count()

        user_response_count = user.user_of_pre_register_task_response.count()

        return (count_of_questions - user_response_count) < 1
