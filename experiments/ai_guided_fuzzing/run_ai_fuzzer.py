from pathlib import Path

from src.fuzzers.ai_fuzzer import generate_ai_inputs
from src.utils.executor import execute_input
from src.utils.result_logger import save_result

TARGET_INPUT_COUNT = 100
MAX_GENERATION_ATTEMPTS = 10
OUTPUT_FILE = "results/logs/ai_fuzzer_results.jsonl"


def clear_previous_results():
    path = Path(OUTPUT_FILE)

    if path.exists():
        path.unlink()


def run_ai_fuzzer():
    clear_previous_results()

    executed_inputs = 0
    generation_attempt = 0

    while executed_inputs < TARGET_INPUT_COUNT and generation_attempt < MAX_GENERATION_ATTEMPTS:
        generation_attempt += 1

        print(f"AI generation attempt {generation_attempt}/{MAX_GENERATION_ATTEMPTS}")

        ai_inputs = generate_ai_inputs()

        if not ai_inputs:
            print("No AI inputs generated in this attempt. Trying again.")
            continue

        for test_input in ai_inputs:
            if executed_inputs >= TARGET_INPUT_COUNT:
                break

            result = execute_input(test_input)
            save_result(result, OUTPUT_FILE)

            executed_inputs += 1

    print(f"AI fuzzer completed: {executed_inputs} inputs")
    print(f"Results saved to: {OUTPUT_FILE}")

    if executed_inputs < TARGET_INPUT_COUNT:
        print(
            f"Warning: only {executed_inputs}/{TARGET_INPUT_COUNT} inputs were completed. "
            "Increase MAX_GENERATION_ATTEMPTS if needed."
        )


if __name__ == "__main__":
    run_ai_fuzzer()