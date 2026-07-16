from pathlib import Path

from src.fuzzers.random_fuzzer import generate_batch
from src.fuzzers.ai_fuzzer import generate_ai_inputs
from src.utils.executor import execute_input
from src.utils.result_logger import save_result

PILOT_INPUT_COUNT = 50
MAX_AI_GENERATION_ATTEMPTS = 8

RANDOM_OUTPUT_FILE = "results/logs/week7_random_pilot_results.jsonl"
AI_OUTPUT_FILE = "results/logs/week7_ai_pilot_results.jsonl"


def clear_previous_results(output_file):
    path = Path(output_file)

    if path.exists():
        path.unlink()

    path.parent.mkdir(parents=True, exist_ok=True)


def run_random_pilot():
    print("Running Week 7 random fuzzer pilot")
    print("----------------------------------")

    clear_previous_results(RANDOM_OUTPUT_FILE)

    random_inputs = generate_batch(PILOT_INPUT_COUNT)

    for test_input in random_inputs:
        result = execute_input(test_input)
        save_result(result, RANDOM_OUTPUT_FILE)

    print(f"Random pilot completed: {PILOT_INPUT_COUNT} inputs")
    print(f"Results saved to: {RANDOM_OUTPUT_FILE}")


def run_ai_pilot():
    print("\nRunning Week 7 AI-guided fuzzer pilot")
    print("-------------------------------------")

    clear_previous_results(AI_OUTPUT_FILE)

    executed_inputs = 0
    generation_attempt = 0

    while executed_inputs < PILOT_INPUT_COUNT and generation_attempt < MAX_AI_GENERATION_ATTEMPTS:
        generation_attempt += 1

        print(f"AI generation attempt {generation_attempt}/{MAX_AI_GENERATION_ATTEMPTS}")

        ai_inputs = generate_ai_inputs()

        if not ai_inputs:
            print("No AI inputs generated in this attempt. Trying again.")
            continue

        for test_input in ai_inputs:
            if executed_inputs >= PILOT_INPUT_COUNT:
                break

            result = execute_input(test_input)
            save_result(result, AI_OUTPUT_FILE)

            executed_inputs += 1

    print(f"AI pilot completed: {executed_inputs} inputs")
    print(f"Results saved to: {AI_OUTPUT_FILE}")

    if executed_inputs < PILOT_INPUT_COUNT:
        print(
            f"Warning: only {executed_inputs}/{PILOT_INPUT_COUNT} AI inputs were completed. "
            "Increase MAX_AI_GENERATION_ATTEMPTS if needed."
        )


def run_week7_pilot():
    run_random_pilot()
    run_ai_pilot()


if __name__ == "__main__":
    run_week7_pilot()