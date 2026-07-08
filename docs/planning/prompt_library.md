# Prompt Library

## Goal

The goal of the prompt library is to define reusable prompts for generating calculator test inputs using a language model.

The model should generate only test inputs, with one input per line and no explanations.

## Output Format Rule

All prompts must follow this output format:

* One test input per line
* No numbering
* No explanations
* No markdown
* No extra text

## Prompt 1: Valid Arithmetic Expressions

Generate 20 valid arithmetic expressions for testing a calculator parser.

Rules:
- Use only numbers, +, -, *, /, and parentheses.
- One expression per line.
- Do not include explanations.
- Do not include numbering.

## Prompt 2: Invalid Arithmetic Expressions

Generate 20 invalid arithmetic expressions for testing parser error handling.

Rules:
- Include malformed syntax.
- Include unbalanced parentheses.
- Include invalid operator combinations.
- One expression per line.
- Do not include explanations.
- Do not include numbering.

## Prompt 3: Division by Zero Cases

Generate 20 arithmetic expressions that may trigger division-by-zero behavior.

Rules:
- Use only numbers, +, -, *, /, and parentheses.
- One expression per line.
- Do not include explanations.
- Do not include numbering.

## Prompt 4: Parentheses-Heavy Expressions

Generate 20 arithmetic expressions with many parentheses.

Rules:
- Include both valid and invalid expressions.
- Use nested parentheses.
- One expression per line.
- Do not include explanations.
- Do not include numbering.

## Prompt 5: Large Number Expressions

Generate 20 arithmetic expressions using very large numbers.

Rules:
- Use addition, subtraction, multiplication, and division.
- Include some edge cases.
- One expression per line.
- Do not include explanations.
- Do not include numbering.

## Prompt 6: Mixed Fuzzing Inputs

Generate 50 calculator fuzzing inputs.

Rules:
- Include valid arithmetic expressions.
- Include invalid arithmetic expressions.
- Include division by zero.
- Include unbalanced parentheses.
- Include large numbers.
- One input per line.
- Do not include explanations.
- Do not include numbering.