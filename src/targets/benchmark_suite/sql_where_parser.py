import re


CONDITION_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*\s*(=|!=|>|<|>=|<=)\s*('[^']*'|\d+)$"
)


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    text = input_string.strip()

    if not text:
        raise ValueError("SQL WHERE condition cannot be empty")

    if text.upper().startswith("WHERE "):
        text = text[6:].strip()

    if not text:
        raise ValueError("Missing condition after WHERE")

    normalized = text.replace(" AND ", " __AND__ ").replace(" OR ", " __OR__ ")
    parts = normalized.split()

    if "__AND__" in parts or "__OR__" in parts:
        conditions = []
        operators = []

        current = []

        for part in parts:
            if part in {"__AND__", "__OR__"}:
                if not current:
                    raise ValueError("Logical operator missing left condition")

                conditions.append(" ".join(current))
                operators.append(part)
                current = []
            else:
                current.append(part)

        if not current:
            raise ValueError("Logical operator missing right condition")

        conditions.append(" ".join(current))

        for condition in conditions:
            if not CONDITION_PATTERN.match(condition):
                raise ValueError("Invalid SQL condition")

        return {
            "valid": True,
            "condition_count": len(conditions),
            "operators": operators,
        }

    if not CONDITION_PATTERN.match(text):
        raise ValueError("Invalid SQL condition")

    return {
        "valid": True,
        "condition_count": 1,
        "operators": [],
    }