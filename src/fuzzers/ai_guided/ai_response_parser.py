import json


def remove_code_fences(text):
    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    return cleaned


def extract_json_object(text):
    """
    Extract the first valid JSON object from a response.

    This tolerates:
    - Markdown code fences
    - explanatory text before JSON
    - trailing text after valid JSON
    """
    cleaned = remove_code_fences(text)
    decoder = json.JSONDecoder()
    errors = []

    for index, character in enumerate(cleaned):
        if character != "{":
            continue

        try:
            parsed, _ = decoder.raw_decode(cleaned[index:])

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError as error:
            errors.append(str(error))

    error_detail = errors[-1] if errors else "No JSON object was found."

    raise ValueError(
        f"AI response did not contain a valid JSON object: {error_detail}"
    )


def parse_generated_inputs(
    response_text,
    expected_count=None,
    max_input_length=500,
):
    if not isinstance(response_text, str):
        raise ValueError("AI response must be a string.")

    parsed = extract_json_object(response_text)
    inputs = parsed.get("inputs")

    if not isinstance(inputs, list):
        raise ValueError(
            'AI response must contain an "inputs" list.'
        )

    cleaned_inputs = []
    seen = set()

    for value in inputs:
        if not isinstance(value, str):
            continue

        if len(value) > max_input_length:
            value = value[:max_input_length]

        if value in seen:
            continue

        seen.add(value)
        cleaned_inputs.append(value)

    if expected_count is not None and len(cleaned_inputs) != expected_count:
        raise ValueError(
            f"Expected {expected_count} unique inputs, "
            f"but received {len(cleaned_inputs)}."
        )

    return cleaned_inputs