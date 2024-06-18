import logging

from kavenegar import KavenegarAPI, APIException, HTTPException
from .models import NotifyLog


API_KEY = '4973593739752F72545932434C7A356C6238623462644544617575596D794E36346E6E71745873357250773D'
logger = logging.getLogger('sms')

def send_authentication_sms(user_phone_number, username, password):
    """
    Sends an SMS containing the user's username and password.

    Args:
        user_phone_number (str or int): The user's phone number.
        username (str): The user's username.
        password (str): The user's password.
    """

    message = f"Username: {username}\nPassword: {password}"

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '10004346',
            'receptor': user_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        status = response['return']['status']
        
        logger.info(f"SMS sent successfully for")
        
        try:
            notify_log_object = NotifyLog.objects.create(
                phone_number=user_phone_number,
                status=status,
                response_data=response
            )
            logger.info(f"NotifyLog object created successfully [uuid:{notify_log_object}]")
        except:
            logger.error(f"Create NotifyLog object failed!: {response}")
            
        
    except APIException as e:
        print("APIException occurred:", e)
    except HTTPException as e:
        print("HTTPException occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def send_welcome_sms(user_phone_number):
    """
    Sends a welcome SMS to the user.

    Args:
        user_phone_number (str or int): The user's phone number.
    """

    message = "Welcome to our service! We're glad to have you with us."

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '10004346',
            'receptor': user_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        print("Welcome SMS sent successfully:", response)
    except APIException as e:
        print("APIException occurred:", e)
    except HTTPException as e:
        print("HTTPException occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def send_event_registration_sms(user_phone_number, event_name, event_date):
    """
    Sends an SMS confirming the user's registration for an event.

    Args:
        user_phone_number (str or int): The user's phone number.
        event_name (str): The name of the event.
        event_date (str): The date of the event.
    """

    # Validate event_name and event_date
    if not isinstance(event_name, str) or not isinstance(event_date, str):
        print("Error: Event name and event date must be strings.")
        return

    message = f"You have successfully registered for {event_name} on {event_date}. Looking forward to seeing you there!"

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '10004346',
            'receptor': user_phone_number,
            'message': message
        }
        response = api.sms_send(params)
        print("Event registration SMS sent successfully:", response)
    except APIException as e:
        print("APIException occurred:", e)
    except HTTPException as e:
        print("HTTPException occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
