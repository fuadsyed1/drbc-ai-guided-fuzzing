import re


TAG_PATTERN = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9_]*)>")


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("XML-like input cannot be empty")

    tags = TAG_PATTERN.findall(input_string)

    if not tags:
        raise ValueError("No XML-like tags found")

    stack = []

    for slash, tag_name in tags:
        if slash == "":
            stack.append(tag_name)
        else:
            if not stack:
                raise ValueError("Closing tag without opening tag")

            opening = stack.pop()

            if opening != tag_name:
                raise ValueError("Mismatched closing tag")

    if stack:
        raise ValueError("Unclosed tag")

    reconstructed = TAG_PATTERN.sub("", input_string)

    if "<" in reconstructed or ">" in reconstructed:
        raise ValueError("Malformed tag syntax")

    return {
        "valid": True,
        "tag_count": len(tags),
        "text_length": len(reconstructed),
    }