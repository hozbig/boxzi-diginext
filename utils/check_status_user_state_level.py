from typing import Union

def level_checker(previous_level: str, new_level: str) -> Union[bool, str]:
    try:
        previous_level = int(previous_level)
    except ValueError:
        return f"previous_level NAN - '{previous_level}' is not a number"
    
    try:
        new_level = int(new_level)
    except ValueError:
        return f"new_level NAN - '{new_level}' is not a number"
    
    if previous_level >= new_level:
        return False
    
    return True


def add_one_level(previous_level: str) -> Union[str, str]:
    try:
        previous_level = int(previous_level)
    except ValueError:
        return f"previous_level NAN - '{previous_level}' is not a number"
    
    new_level = previous_level + 1

    if level_checker(previous_level, new_level):
        return str(new_level)
    return str(previous_level)
