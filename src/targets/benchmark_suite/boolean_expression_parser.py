VALID_TOKENS = {"TRUE", "FALSE", "AND", "OR", "NOT", "(", ")"}


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    text = input_string.strip()

    if not text:
        raise ValueError("Boolean expression cannot be empty")

    spaced = text.replace("(", " ( ").replace(")", " ) ")
    tokens = spaced.split()

    if not tokens:
        raise ValueError("Boolean expression cannot be empty")

    for token in tokens:
        if token not in VALID_TOKENS:
            raise ValueError("Invalid boolean token")

    if tokens.count("(") != tokens.count(")"):
        raise ValueError("Unbalanced parentheses")

    expecting_value = True
    value_count = 0
    operator_count = 0

    for token in tokens:
        if token == "(":
            continue

        if token == ")":
            continue

        if expecting_value:
            if token == "NOT":
                continue

            if token not in {"TRUE", "FALSE"}:
                raise ValueError("Expected boolean value")

            value_count += 1
            expecting_value = False

        else:
            if token not in {"AND", "OR"}:
                raise ValueError("Expected boolean operator")

            operator_count += 1
            expecting_value = True

    if expecting_value:
        raise ValueError("Expression ended unexpectedly")

    return {
        "valid": True,
        "token_count": len(tokens),
        "value_count": value_count,
        "operator_count": operator_count,
    }