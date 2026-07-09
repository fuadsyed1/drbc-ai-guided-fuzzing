from src.utils.ai_generator import generate_inputs
from src.utils.ai_validator import clean_ai_output


DEFAULT_PROMPT = """
Generate 20 calculator fuzzing inputs.

Rules:
- Use numbers, +, -, *, /, and parentheses.
- Include valid arithmetic expressions.
- Include invalid arithmetic expressions.
- Include division by zero cases.
- Include parentheses-heavy expressions.
- Include large number expressions.
- One input per line.
- Do not explain.
- Do not use markdown.
"""


def generate_ai_inputs(prompt=DEFAULT_PROMPT):
    raw_output = generate_inputs(prompt)
    return clean_ai_output(raw_output)


if __name__ == "__main__":
    ai_inputs = generate_ai_inputs()

    print("AI Generated Inputs")
    print("-------------------")

    for item in ai_inputs:
        print(item)