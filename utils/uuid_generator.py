import string
import uuid

from django.utils.crypto import get_random_string

def random_uuid4():
    return uuid.uuid4()

def random_uuid(max_char=5):
    """
    Generates a string containing random characters in [max_char] characters.
    """
    all_digits = string.digits
    all_lowercase_characters = string.ascii_lowercase
    return get_random_string(
        length=max_char, allowed_chars=all_digits + all_lowercase_characters
    )