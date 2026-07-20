import re


USERNAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{2,19}$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("Username cannot be empty")

    if len(input_string) < 3:
        raise ValueError("Username is too short")

    if len(input_string) > 20:
        raise ValueError("Username is too long")

    if not USERNAME_PATTERN.match(input_string):
        raise ValueError("Invalid username format")

    reserved_names = {"admin", "root", "system", "null"}

    if input_string.lower() in reserved_names:
        raise ValueError("Username is reserved")

    return {
        "valid": True,
        "username": input_string,
        "length": len(input_string),
    }