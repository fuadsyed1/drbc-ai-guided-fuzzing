import re


ALLOWED_VARIABLES = {
    "name": "Alice",
    "date": "2026-01-01",
    "greeting": "Hello",
}


PLACEHOLDER_PATTERN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string:
        raise ValueError("Template cannot be empty")

    if input_string.count("{") != input_string.count("}"):
        raise ValueError("Unbalanced template braces")

    placeholders = PLACEHOLDER_PATTERN.findall(input_string)

    if "{" in input_string or "}" in input_string:
        rebuilt = PLACEHOLDER_PATTERN.sub("", input_string)

        if "{" in rebuilt or "}" in rebuilt:
            raise ValueError("Invalid placeholder syntax")

    rendered = input_string

    for placeholder in placeholders:
        if placeholder not in ALLOWED_VARIABLES:
            raise KeyError(f"Unknown template variable: {placeholder}")

        rendered = rendered.replace(
            "{" + placeholder + "}",
            ALLOWED_VARIABLES[placeholder],
        )

    return {
        "valid": True,
        "placeholder_count": len(placeholders),
        "rendered": rendered,
    }