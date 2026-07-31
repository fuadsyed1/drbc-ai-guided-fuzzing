MAX_INPUT_LENGTH = 500
MAX_DIGIT_RUN_FOR_ARITHMETIC = 30

ARITHMETIC_TARGETS = {
    "calculator",
    "arithmetic_script_parser",
}


def has_long_digit_run(value, max_run=MAX_DIGIT_RUN_FOR_ARITHMETIC):
    current_run = 0

    for character in value:
        if character.isdigit():
            current_run += 1

            if current_run > max_run:
                return True
        else:
            current_run = 0

    return False


def validate_ai_input(target_name, value):
    """
    Validate one AI-generated input before target execution.

    Returns:
        (True, None) when accepted
        (False, reason) when rejected
    """
    if not isinstance(value, str):
        return False, "Input is not a string."

    if len(value) > MAX_INPUT_LENGTH:
        return False, f"Input exceeds {MAX_INPUT_LENGTH} characters."

    if target_name in ARITHMETIC_TARGETS:
        if "**" in value:
            return False, "Exponentiation is blocked for safety."

        if has_long_digit_run(value):
            return False, "Input contains an excessively long numeric literal."

    return True, None


def filter_ai_inputs(target_name, inputs):
    accepted = []
    rejected = []

    for value in inputs:
        is_valid, reason = validate_ai_input(target_name, value)

        if is_valid:
            accepted.append(value)
        else:
            rejected.append({
                "input": value,
                "reason": reason,
            })

    return accepted, rejected