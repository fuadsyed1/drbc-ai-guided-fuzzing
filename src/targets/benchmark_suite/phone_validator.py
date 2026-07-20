import re


PHONE_PATTERNS = [
    re.compile(r"^\d{3}-\d{3}-\d{4}$"),
    re.compile(r"^\(\d{3}\)\d{3}-\d{4}$"),
    re.compile(r"^\+1-\d{3}-\d{3}-\d{4}$"),
]


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("Phone number cannot be empty")

    if len(input_string) > 20:
        raise ValueError("Phone number is too long")

    for pattern in PHONE_PATTERNS:
        if pattern.match(input_string):
            digits = re.sub(r"\D", "", input_string)
            return {
                "valid": True,
                "digits": digits,
                "digit_count": len(digits),
            }

    raise ValueError("Invalid phone number format")