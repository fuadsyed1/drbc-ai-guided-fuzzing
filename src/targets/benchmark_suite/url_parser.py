from urllib.parse import urlparse


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("URL cannot be empty")

    parsed = urlparse(input_string)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    if "." not in parsed.netloc:
        raise ValueError("URL domain must contain a dot")

    return {
        "valid": True,
        "scheme": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
    }