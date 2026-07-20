VALID_METHODS = {"GET", "POST", "PUT", "DELETE"}
VALID_VERSIONS = {"HTTP/1.0", "HTTP/1.1", "HTTP/2"}


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("HTTP request cannot be empty")

    lines = input_string.replace("\r\n", "\n").split("\n")

    request_line = lines[0].strip()
    parts = request_line.split()

    if len(parts) != 3:
        raise ValueError("HTTP request line must contain method, path, and version")

    method, path, version = parts

    if method not in VALID_METHODS:
        raise ValueError("Invalid HTTP method")

    if not path.startswith("/"):
        raise ValueError("HTTP path must start with /")

    if version not in VALID_VERSIONS:
        raise ValueError("Invalid HTTP version")

    headers = {}

    for line in lines[1:]:
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            raise ValueError("Invalid HTTP header format")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError("HTTP header key cannot be empty")

        if not value:
            raise ValueError("HTTP header value cannot be empty")

        headers[key] = value

    if "Host" not in headers:
        raise ValueError("HTTP request must include Host header")

    return {
        "valid": True,
        "method": method,
        "path": path,
        "version": version,
        "header_count": len(headers),
    }