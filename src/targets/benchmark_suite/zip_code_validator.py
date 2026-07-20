import re


ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("ZIP code cannot be empty")

    if not ZIP_PATTERN.match(input_string):
        raise ValueError("Invalid ZIP code format")

    return {
        "valid": True,
        "zip_code": input_string,
        "extended": "-" in input_string,
    }