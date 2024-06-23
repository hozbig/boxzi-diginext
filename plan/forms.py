from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Plan


class PlanCreateForm(ModelForm):
    class Meta:
        model = Plan
        exclude = ("created_time", "last_update_time", "likes")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields["pitch_deck"].widget.attrs['accept'] = 'application/pdf'
        self.fields["video"].widget.attrs['accept'] = 'video/*'
        
    def clean_pitch_deck(self):
        pitch_deck = self.cleaned_data.get('pitch_deck')
        if pitch_deck and not pitch_deck.name.endswith('.pdf'):
            raise ValidationError('فقط فایل‌های PDF مجاز هستند')
        return pitch_deck

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.content_type.startswith('video'):
                raise ValidationError('فقط فایل‌های ویدیویی مجاز هستند')
            if video.size > 25 * 1024 * 1024: 
                raise ValidationError('حجم فایل ویدیویی نباید بیشتر از 50MB باشد')
        return video
