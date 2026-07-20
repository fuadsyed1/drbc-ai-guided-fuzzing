from urllib.parse import parse_qsl


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Query string cannot be empty")

    cleaned = input_string[1:] if input_string.startswith("?") else input_string

    if not cleaned:
        raise ValueError("Query string has no parameters")

    if "&&" in cleaned:
        raise ValueError("Query string contains empty parameter")

    pairs = parse_qsl(cleaned, keep_blank_values=True)

    if not pairs:
        raise ValueError("No query parameters found")

    result = {}

    for key, value in pairs:
        if not key:
            raise ValueError("Query parameter key cannot be empty")

        if value == "":
            raise ValueError("Query parameter value cannot be empty")

        if key in result:
            raise ValueError("Duplicate query parameter key")

        result[key] = value

    return {
        "valid": True,
        "parameters": result,
        "parameter_count": len(result),
    }