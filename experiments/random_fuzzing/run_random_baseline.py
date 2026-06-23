from pathlib import Path

from src.fuzzers.random_fuzzer import generate_batch
from src.utils.executor import execute_input
from src.utils.result_logger import save_result


OUTPUT_FILE = "results/logs/random_baseline_results.jsonl"


def clear_previous_results():
    path = Path(OUTPUT_FILE)

    if path.exists():
        path.unlink()


def run_random_baseline(total_inputs=100):
    clear_previous_results()

    for test_input in generate_batch(total_inputs):
        result = execute_input(test_input)
        save_result(result, OUTPUT_FILE)

    print(f"Random baseline completed: {total_inputs} inputs")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_random_baseline(100)