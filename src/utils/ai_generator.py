import subprocess


MODEL = "qwen3:1.7b"


def generate_inputs(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=120,
        )

        return result.stdout

    except Exception as error:
        print(f"AI generation failed: {error}")
        return ""