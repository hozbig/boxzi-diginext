import logging
import random
# import json

from kavenegar import KavenegarAPI
from .models import NotifyLog, OTP


API_KEY = '5942524C707361635633774F54767244524A314C5856564A3367416464446F33'
SENDER_NUMBER = '10000018121812'

logger = logging.getLogger('sms')


messages = {
    # {name}
    "invitation_to_jury": "{first_name} عزیز، خوشحال و مفتخریم که شما رو در تیم داوری این رویداد همراهمون داریم.",
    
    # {name}
    "interview_acceptance": "{first_name} عزیز، شما برای مرحله مصاحبه پذیرفته شدید. برای رزرو زمان مصاحبه به پنل کاربریتون مراجعه کنید.",
    
    # {name}
    "summer_camp_acceptance": "{first_name} عزیز، تبریک! پس از بررسی‌های صورت گرفته توسط تیم داوری دیجی‌نکست، شما برای ورود به کمپ تابستانی دیجی‌نکست پذیرفته شدید. برای اطلاع از سایر مراحل،‌ می‌تونید به پنل کاربریتون مراجعه کنید.",
    
    # {name}
    "summer_camp_rejection": "{first_name} عزیز، بعد از بررسی‌های صورت گرفته توسط داورهای کمپ تابستانی دیجی‌نکست، متاسفانه افتخار میزبانی از شما رو نداریم. به امید دیدار مجدد در کمپ‌های آینده!",
    
    # {name}
    "summer_camp_watched": "{first_name} عزیز، درخواست شما برای ورود به کمپ تابستانی دیجی نکست دردست بررسی توسط داوران ما می‌باشد!",
    
    "initial_registration_success": "همراه گرامی، ثبت‌نام اولیه شما در کمپ تابستانی دیجی‌نکست با موفقیت انجام شد.",
    
    "final_registration_success": "به باکس‌زی خوش آمدید! برای ثبت نام در نهمین کمپ استارتاپی دیجی‌نکست داخل پلتفرم مراحل را طی کرده و چالش های خود را انجام دهید.",
    
    "complete_road_registration": "همراه گرامی، درخواست شما برای ورود به کمپ تابستانی دیجی نکست با موفقیت ارسال شد.",
    
    # {name} - {team_name}
    "team_addition": "سلام به کمپ تابستانی دیجی‌نکست خوش آمدید. {first_name} جان شما به عنوان هم‌تیمی به تیم {team_name} اضافه شدید.",
    
    # {name} - {username} - {password}
    "username_password":
                   "نام کاربری: {phone_number}\n"
                   "رمز عبور: {password}\n\n"
                   "از پنل باکس‌زی وارد شوید .\n\n"
                   "https://diginext.boxzi.ir"
}

def send_messages(action, destination_phone_number, user=None, team_name="", password=""):    
    # Get the message template
    message_template = messages[action]
    
    # Fill in the data into the message template
    if action == "team_addition":
        message = message_template.format(first_name=user, team_name=team_name)
    elif action == "username_password":
        message = message_template.format(first_name=user, password=password, phone_number=destination_phone_number)
    else:
        message = message_template.format(first_name=user)
    
    api = KavenegarAPI(API_KEY)
    params = {
        'sender': SENDER_NUMBER,
        'receptor': destination_phone_number,
        'message': message
    }
    
    try:
        api.sms_send(params)
    except:
        pass


def send_otp(phone_number, otp_code):    
    api = KavenegarAPI(API_KEY)

    message = f"""کد یکبار مصرف برای ورود به باکس‌زی
CODE: {otp_code}
"""

    params = {
        'sender': SENDER_NUMBER,
        'receptor': phone_number,
        'message': message
    }

    try:
        api.sms_send(params)
    except:
        pass

def generate_otp():
    return str(random.randint(100000, 999999))
