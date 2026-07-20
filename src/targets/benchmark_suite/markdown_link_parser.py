import re


MARKDOWN_LINK_PATTERN = re.compile(r"^\[([^\]]+)\]\((https?://[^)\s]+)\)$")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Markdown link cannot be empty")

    match = MARKDOWN_LINK_PATTERN.match(input_string)

    if not match:
        raise ValueError("Invalid markdown link format")

    text = match.group(1)
    url = match.group(2)

    if not text.strip():
        raise ValueError("Markdown link text cannot be empty")

    if "." not in url:
        raise ValueError("Markdown URL must contain a domain")

    return {
        "valid": True,
        "text": text,
        "url": url,
    }