import re


ALLOWED_CHARS = set("0123456789+-*/() ")


def is_calculator_input(line):
    if not line:
        return False

    if len(line) > 80:
        return False

    if not any(char.isdigit() for char in line):
        return False

    return all(char in ALLOWED_CHARS for char in line)


def clean_line(line):
    line = line.strip()

    line = re.sub(r"^\d+[\.\)]\s*", "", line)
    line = re.sub(r"^[-*]\s*", "", line)

    return line.strip()


def clean_ai_output(raw_output):
    cleaned = []
    seen = set()

    for line in raw_output.splitlines():
        line = clean_line(line)

        if not is_calculator_input(line):
            continue

        if line in seen:
            continue

        seen.add(line)
        cleaned.append(line)

    return cleaned