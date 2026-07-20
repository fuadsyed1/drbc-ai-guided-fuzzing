import string


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if len(input_string) < 8:
        raise ValueError("Password is too short")

    if len(input_string) > 64:
        raise ValueError("Password is too long")

    if not any(char.islower() for char in input_string):
        raise ValueError("Password must contain a lowercase letter")

    if not any(char.isupper() for char in input_string):
        raise ValueError("Password must contain an uppercase letter")

    if not any(char.isdigit() for char in input_string):
        raise ValueError("Password must contain a digit")

    if not any(char in string.punctuation for char in input_string):
        raise ValueError("Password must contain a symbol")

    common_passwords = {"password", "password1", "admin123", "qwerty123"}

    if input_string.lower() in common_passwords:
        raise ValueError("Password is too common")

    return {
        "valid": True,
        "length": len(input_string),
        "strength": "strong",
    }