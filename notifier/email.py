import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)

def send_email(user, template, password=""):
    valid_template_name_list = [
        "welcome",
        "authentication_info", # Send authentication information
    ]

    if template not in valid_template_name_list:
        logger.error(f"Invalid template name: '{template}'!")

    subject = 'به باکس زی خوش آمدید!'
    html_message = render_to_string(f'email/{template}.html', {'user': user, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = 'diginext@boxzi.ir'
    to_email = [user.email]

    email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    
    try:
        email.send()
    except Exception as e:
        # Log the error
        logger.error("Failed to send email to user with email %s. Error: %s", user.email, str(e))
