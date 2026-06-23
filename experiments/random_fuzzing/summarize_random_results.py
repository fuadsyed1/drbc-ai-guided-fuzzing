import json
from collections import Counter
from pathlib import Path


RESULT_FILE = "results/logs/random_baseline_results.jsonl"
SUMMARY_FILE = "results/logs/random_baseline_summary.json"


def load_results(path):
    file_path = Path(path)

    if not file_path.exists():
        print(f"Result file not found: {path}")
        return []

    with file_path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def summarize_results(results):
    total = len(results)
    passed = sum(1 for item in results if item["status"] == "PASS")
    crashed = sum(1 for item in results if item["status"] == "CRASH")

    error_types = Counter(
        item["error_type"]
        for item in results
        if item["error_type"] is not None
    )

    avg_time = 0
    if total > 0:
        avg_time = sum(item["execution_time"] for item in results) / total

    return {
        "total_inputs": total,
        "valid_inputs": passed,
        "crash_error_inputs": crashed,
        "average_execution_time": avg_time,
        "unique_error_types": dict(error_types),
    }


def save_summary(summary):
    path = Path(SUMMARY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)


def print_summary(summary):
    print("\nRandom Baseline Summary")
    print("-----------------------")
    print(f"Total inputs: {summary['total_inputs']}")
    print(f"Valid inputs: {summary['valid_inputs']}")
    print(f"Crash/error inputs: {summary['crash_error_inputs']}")
    print(
        "Average execution time: "
        f"{summary['average_execution_time']:.8f} seconds"
    )

    print("\nUnique error types:")
    for error_type, count in summary["unique_error_types"].items():
        print(f"- {error_type}: {count}")


if __name__ == "__main__":
    data = load_results(RESULT_FILE)
    summary_data = summarize_results(data)
    save_summary(summary_data)
    print_summary(summary_data)
    print(f"\nSummary saved to: {SUMMARY_FILE}")