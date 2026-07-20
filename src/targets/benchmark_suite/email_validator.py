import re


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("Email cannot be empty")

    if len(input_string) > 254:
        raise ValueError("Email is too long")

    if input_string.count("@") != 1:
        raise ValueError("Email must contain exactly one @ symbol")

    if not EMAIL_PATTERN.match(input_string):
        raise ValueError("Invalid email format")

    local_part, domain = input_string.split("@")

    if local_part.startswith(".") or local_part.endswith("."):
        raise ValueError("Invalid local part")

    if ".." in input_string:
        raise ValueError("Email cannot contain consecutive dots")

    return {
        "valid": True,
        "local_part": local_part,
        "domain": domain,
    }