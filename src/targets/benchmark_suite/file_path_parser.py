INVALID_CHARS = set("<>|?*")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("File path cannot be empty")

    if any(char in INVALID_CHARS for char in input_string):
        raise ValueError("File path contains invalid characters")

    if "\0" in input_string:
        raise ValueError("File path contains null byte")

    normalized = input_string.replace("\\", "/")

    parts = [part for part in normalized.split("/") if part]

    if not parts:
        raise ValueError("File path contains no valid parts")

    filename = parts[-1]

    if filename in {".", ".."}:
        raise ValueError("File path must end with a file name")

    if "." not in filename:
        raise ValueError("File path should include a file extension")

    return {
        "valid": True,
        "path": input_string,
        "parts": parts,
        "filename": filename,
        "depth": len(parts),
    }