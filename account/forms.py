from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm, ModelMultipleChoiceField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from hcaptcha.fields import hCaptchaField

from .models import User, Meeting, LeanCanvas, WorkExperience


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        validators=[
            RegexValidator(
                r'^09\d{9}$',
                message='شماره تماس باید با 09 شروع شده و شامل 11 رقم باشد. مطمئن شوید که از اعداد لاتین استفاده میکنید!',
            )
        ]
    )
    password = forms.CharField(widget=forms.PasswordInput)
    hcaptcha = hCaptchaField()
    
    phone_number.widget.attrs["placeholder"] = "جهت ورود شماره موبایل خودرا وارد کنید"
    phone_number.widget.attrs["class"] = "phoneInput"
    password.widget.attrs["placeholder"] = "············"
    password.label = ""


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "email",
        )


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "degree",
            "interests",
            "abilities",
            "bio",
            "college_name",
            "province",
            "city",
            "number_id",
        )
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True  # Make each field required
            if isinstance(field, forms.ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'


class MeetingCreateForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ("created_time", "last_update_time", "status", "rate", "uuid")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class WorkExperienceCreateForm(ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ("created_time", "last_update_time", "uuid")


class LeanCanvasForm(ModelForm):
    class Meta:
        model = LeanCanvas
        exclude = ("created_time", "last_update_time", "uuid")


class UserLoginOrRegisterForm(ModelForm):
    phone_number = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                r'^09\d{9}$',
                message='شماره تماس باید با 09 شروع شده و شامل 11 رقم باشد. مطمئن شوید که از اعداد لاتین استفاده میکنید!'
            )
        ]
    )

    class Meta(UserCreationForm):
        model = User
        fields = (
            "phone_number",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        # Remove labels and add placeholders
        self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره تماس *'
        self.fields['phone_number'].widget.attrs['style'] = 'text-align:right'
        self.fields['phone_number'].widget.attrs["class"] = "phoneInput"
        # Remove labels
        self.fields['phone_number'].label = ''


class UserRegisterFormLevel1(UserCreationForm):
    phone_number = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                r'^09\d{9}$',
                message='شماره تماس باید با 09 شروع شده و شامل 11 رقم باشد. مطمئن شوید که از اعداد لاتین استفاده میکنید!'
            )
        ]
    )
    hcaptcha = hCaptchaField()

    class Meta(UserCreationForm):
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "accept_nda",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change placeholders
        self.fields['email'].widget.attrs['placeholder'] = "* " + self.fields["email"].label
        # self.fields['phone_number'].widget.attrs['placeholder'] = "* " + self.fields["phone_number"].label
        self.fields['password1'].widget.attrs['placeholder'] = "* " + self.fields["password1"].label
        self.fields['password2'].widget.attrs['placeholder'] = "* " + self.fields["password2"].label
        self.fields['first_name'].widget.attrs['placeholder'] = "* " + self.fields["first_name"].label
        self.fields['last_name'].widget.attrs['placeholder'] = "* " + self.fields["last_name"].label
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'text-align:right'
        # Remove/Change help_text
        self.fields['accept_nda'].label = "قوانین سایت را مطالعه و قبول دارم."
        self.fields['password1'].help_text = 'گذرواژه شما باید حداقل ۸ حرف داشته باشد، نباید مشابه اطلاعات شخصی، یک رمز عبور معمول یا فقط عدد باشد'
        self.fields['password2'].help_text = ''


class UserRegisterFormLevel2(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "birthday",
            "degree",
            "college_name",
            "province",
            "city",
        )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Change placeholders to fields
        self.fields['birthday'].widget.attrs['placeholder'] = "* " + self.fields["birthday"].label
        # TODO: مدرک تحصیلی و نام دانشگاه دریافت شود
        self.fields['degree'].widget.attrs['placeholder'] = "* " + self.fields["degree"].label
        self.fields['college_name'].widget.attrs['placeholder'] = "* " + self.fields["college_name"].label
        self.fields['province'].widget.attrs['placeholder'] = "* " + self.fields["province"].label
        self.fields['city'].widget.attrs['placeholder'] = "* " + self.fields["city"].label
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'text-align:right'


class UserRegisterFormLevel3(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "type",
            "specialty",
            "programming_language",
            "other_specialties",
            "resume_file",
        )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'text-align:right'
        self.fields["other_specialties"].required = False
        self.fields["resume_file"].widget.attrs['accept'] = 'application/pdf'  # Restrict file input to PDF files

    def clean_resume_file(self):
        resume_file = self.cleaned_data.get('resume_file')
        if resume_file and not resume_file.name.endswith('.pdf'):
            raise ValidationError('فقط فایل‌های PDF مجاز هستند')
        return resume_file


class UserRegisterFormLevel4(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "is_accelerator_experience",
            "if_is_accelerator_experience",
            "is_startup_experience",
            "if_is_startup_experience",
            "why_us",
            "why_us_video",
        )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'text-align:right'
        self.fields["if_is_accelerator_experience"].required = False
        self.fields["if_is_startup_experience"].required = False
        self.fields["why_us"].required = False
        self.fields["why_us_video"].required = False
        self.fields["why_us_video"].widget.attrs['accept'] = 'video/*'
        
    def clean_why_us_video(self):
        why_us_video = self.cleaned_data.get('why_us_video')
        if why_us_video:
            if not why_us_video.content_type.startswith('video'):
                raise ValidationError('فقط فایل‌های ویدیویی مجاز هستند')
            if why_us_video.size > 25 * 1024 * 1024: 
                raise ValidationError('حجم فایل ویدیویی نباید بیشتر از 50MB باشد')
        return why_us_video
    
    def clean(self):
        cleaned_data = super().clean()
        why_us = cleaned_data.get("why_us")
        why_us_video = cleaned_data.get("why_us_video")

        if not why_us and not why_us_video:
            raise ValidationError('لطفاً یکی از فیلدهای "چرا ما" یا "ویدئوی چرا ما" را پر کنید')

        return cleaned_data


class AddRefereeForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                r'^09\d{9}$',
                message='شماره تماس باید با 09 شروع شده و شامل 11 رقم باشد.'
            )
        ], required=True, label="شماره همراه"
    )
    email = forms.EmailField(required=True, label="ایمیل")
    first_name = forms.CharField(max_length=30, required=True, label="نام")
    last_name = forms.CharField(max_length=30, required=True, label="نام خانوادگی")
    referee_validity_date = forms.DateField(required=True, label="تاریخ دسترسی داور تا")
    
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "referee_type",
            "referee_validity_date",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'