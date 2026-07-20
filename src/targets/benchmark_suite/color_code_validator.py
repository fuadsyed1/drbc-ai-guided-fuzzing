import re


HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("Color code cannot be empty")

    if not HEX_COLOR_PATTERN.match(input_string):
        raise ValueError("Invalid hex color code")

    red = int(input_string[1:3], 16)
    green = int(input_string[3:5], 16)
    blue = int(input_string[5:7], 16)

    return {
        "valid": True,
        "red": red,
        "green": green,
        "blue": blue,
    }