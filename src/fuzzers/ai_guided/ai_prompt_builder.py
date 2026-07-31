import json


SYSTEM_PROMPT = """
You are an AI input generator for an authorized software-testing experiment.

Generate diverse test inputs for the described target program.

Requirements:
- Return valid JSON only.
- Use exactly this structure: {"inputs": ["input 1", "input 2"]}
- Return exactly the requested number of inputs.
- Every input must be a string.
- Do not include explanations, Markdown, numbering, or code fences.
- Do not repeat inputs listed in the exclusion list.
- Include normal, boundary, malformed, and error-triggering inputs.
- Keep every input within the requested maximum length.
""".strip()


GENERATION_THEMES = [
    "typical valid inputs with structural variation",
    "empty, minimal, and extremely short inputs",
    "boundary values and off-by-one variations",
    "malformed syntax and missing components",
    "unexpected whitespace, tabs, and line breaks",
    "case changes and mixed capitalization",
    "repeated delimiters and duplicated tokens",
    "unexpected token order and token combinations",
    "numeric boundaries, signs, decimals, and leading zeros",
    "nested structures and unmatched delimiters",
    "longer inputs near the maximum useful size",
    "mutations of seed inputs without copying them exactly",
    "unusual punctuation and symbol combinations",
    "partially valid inputs that fail late in parsing",
    "inputs designed to explore uncommon program branches",
]


def build_generation_prompt(
    target,
    input_count=10,
    max_input_length=500,
    trial_number=1,
    round_number=1,
    existing_inputs=None,
):
    """
    Build a target-aware and round-aware generation prompt.
    """
    existing_inputs = existing_inputs or []

    theme_index = (round_number - 1) % len(GENERATION_THEMES)
    generation_theme = GENERATION_THEMES[theme_index]

    # Keep the prompt manageable while still showing recent duplicates
    # that the model must avoid.
    exclusion_inputs = existing_inputs[-100:]

    metadata = {
        "target_name": target["name"],
        "difficulty": target["difficulty"],
        "category": target["category"],
        "tokens": target.get("tokens", []),
        "seed_inputs": target.get("seeds", []),
        "known_edge_cases": target.get("edge_cases", []),
    }

    user_prompt = f"""
Generate fuzzing inputs for this target:

{json.dumps(metadata, indent=2)}

Experiment settings:
- trial_number: {trial_number}
- generation_round: {round_number}
- required_input_count: {input_count}
- maximum_characters_per_input: {max_input_length}
- primary_generation_theme: {generation_theme}

Already generated inputs that must not be repeated:

{json.dumps(exclusion_inputs, indent=2)}

Generation requirements:
- Generate exactly {input_count} new and unique strings.
- Do not copy anything from the exclusion list.
- Do not simply repeat the provided seed inputs.
- Concentrate on the primary generation theme for this round.
- Make each input meaningfully different from the others.
- Include both successful and error-triggering possibilities.
- Preserve special characters as literal JSON string content.

Return exactly:

{{"inputs": ["...", "..."]}}
""".strip()

    return SYSTEM_PROMPT, user_prompt