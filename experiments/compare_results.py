import json
from pathlib import Path


RANDOM_SUMMARY = "results/logs/random_baseline_summary.json"
AI_SUMMARY = "results/logs/ai_fuzzer_summary.json"


def load_summary(path):
    file_path = Path(path)

    if not file_path.exists():
        print(f"Missing summary file: {path}")
        return None

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def print_comparison(random_data, ai_data):
    print("\nRandom Fuzzer vs AI-Guided Fuzzer")
    print("---------------------------------")
    print(f"{'Metric':<25}{'Random':<15}{'AI-Guided':<15}")
    print("-" * 55)

    metrics = [
        ("Total Inputs", "total_inputs"),
        ("Valid Inputs", "valid_inputs"),
        ("Crash/Error Inputs", "crash_error_inputs"),
        ("Avg Execution Time", "average_execution_time"),
    ]

    for label, key in metrics:
        random_value = random_data.get(key, 0)
        ai_value = ai_data.get(key, 0)

        if key == "average_execution_time":
            random_value = f"{random_value:.8f}"
            ai_value = f"{ai_value:.8f}"

        print(f"{label:<25}{random_value!s:<15}{ai_value!s:<15}")

    print("\nRandom Error Types:")
    for error_type, count in random_data.get("unique_error_types", {}).items():
        print(f"- {error_type}: {count}")

    print("\nAI Error Types:")
    for error_type, count in ai_data.get("unique_error_types", {}).items():
        print(f"- {error_type}: {count}")


if __name__ == "__main__":
    random_summary = load_summary(RANDOM_SUMMARY)
    ai_summary = load_summary(AI_SUMMARY)

    if random_summary and ai_summary:
        print_comparison(random_summary, ai_summary)