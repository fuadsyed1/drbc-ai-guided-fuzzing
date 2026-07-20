import json


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("JSON input cannot be empty")

    try:
        parsed = json.loads(input_string)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON format: {error.msg}")

    if not isinstance(parsed, dict):
        raise ValueError("JSON input must be an object")

    if not parsed:
        raise ValueError("JSON object cannot be empty")

    return {
        "valid": True,
        "keys": list(parsed.keys()),
        "key_count": len(parsed),
    }