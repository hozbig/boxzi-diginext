import logging
import json

from kavenegar import KavenegarAPI, APIException, HTTPException
from .models import NotifyLog


API_KEY = '5942524C707361635633774F54767244524A314C5856564A3367416464446F33'
SENDER_NUMBER = '10000018121812'

logger = logging.getLogger('sms')


def send_authentication_sms(destination_phone_number, password):
    message = f"""
    به باکس زی خوش آمدید!
    
    اطلاعات ورود به حساب خود:
    رمزعبور: {password}
    نام کاربری شما همان شماره موبایل شما میباشد
    """

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER_NUMBER,
            'receptor': destination_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        json_response = json.loads(response)
        status = json_response['return']['status']
        logger.info(f"SMS request sent successfully")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                status=status,
                message=json_response,
                send_try=1
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
        
    except APIException as e:
        logger.error(f"APIException occurred: {e}")
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def send_authentication_sms_referee(destination_phone_number, password):
    message = f"""
    به باکس زی خوش آمدید!
    
    اطلاعات ورود به حساب خود:
    رمزعبور: {password}
    نام کاربری شما همان شماره موبایل شما میباشد
    """

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER_NUMBER,
            'receptor': destination_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        json_response = json.loads(response)
        status = json_response['return']['status']
        logger.info(f"SMS request sent successfully")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                status=status,
                message=json_response,
                send_try=1
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
        
    except APIException as e:
        logger.error(f"APIException occurred: {e}")
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def send_welcome_sms(destination_phone_number, user_name):
    """
    Sends a welcome SMS to the user.

    Args:
        destination_phone_number (str or int): The user's phone number.
    """
    message = f"""
    به باکس زی خوش آمدید!
    
    {user_name} عزیز حساب شما با موفقیت ساخته شد.
    """

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER_NUMBER,
            'receptor': destination_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        json_response = json.loads(response)
        status = json_response['return']['status']
        logger.info(f"Welcome SMS request sent successfully")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                status=status,
                message=json_response,
                send_try=1
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
        
    except APIException as e:
        logger.error(f"APIException occurred: {e}")
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def send_event_registration_sms(destination_phone_number, event_name):
    """
    Sends an SMS confirming the user's registration for an event.

    Args:
        destination_phone_number (str or int): The user's phone number.
        event_name (str): The name of the event.
        event_date (str): The date of the event.
    """
    message = f"""
    تکمیل ثبت نام شما در برنامه {event_name} به صورت کامل انجام شد.
    
    پاسخ شتابدهنده و وضعیت درخواست شما برای شما ارسال خواهد شد.
    """

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER_NUMBER,
            'receptor': destination_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        json_response = json.loads(response)
        status = json_response['return']['status']
        logger.info(f"Road complete registration SMS request sent successfully")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                status=status,
                message=json_response,
                send_try=1
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
        
    except APIException as e:
        logger.error(f"APIException occurred: {e}")
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def custom_message_sms(destination_phone_number, message):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER_NUMBER,
            'receptor': destination_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        json_response = json.loads(response)
        status = json_response['return']['status']
        logger.info(f"Road complete registration SMS request sent successfully")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                status=status,
                message=json_response,
                send_try=1
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
        
    except APIException as e:
        logger.error(f"APIException occurred: {e}")
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

