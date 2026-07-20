import re


PLAIN_LOG_PATTERN = re.compile(r"^(INFO|WARN|ERROR):\s+.+$")
BRACKET_LOG_PATTERN = re.compile(r"^\[(INFO|WARN|ERROR)\]\s+.+$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Log line cannot be empty")

    plain_match = PLAIN_LOG_PATTERN.match(input_string)
    bracket_match = BRACKET_LOG_PATTERN.match(input_string)

    if not plain_match and not bracket_match:
        raise ValueError("Invalid log line format")

    level = plain_match.group(1) if plain_match else bracket_match.group(1)

    message = input_string.split("]", 1)[-1] if input_string.startswith("[") else input_string.split(":", 1)[1]
    message = message.strip()

    if not message:
        raise ValueError("Log message cannot be empty")

    return {
        "valid": True,
        "level": level,
        "message": message,
    }