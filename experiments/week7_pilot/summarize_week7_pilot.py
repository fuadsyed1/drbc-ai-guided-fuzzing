import json
from collections import Counter
from pathlib import Path

RANDOM_RESULTS_FILE = "results/logs/week7_random_pilot_results.jsonl"
AI_RESULTS_FILE = "results/logs/week7_ai_pilot_results.jsonl"
SUMMARY_OUTPUT_FILE = "results/logs/week7_pilot_summary.json"


def load_jsonl(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Missing result file: {file_path}")

    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def get_input_value(record):
    return (
        record.get("input")
        or record.get("test_input")
        or record.get("generated_input")
        or ""
    )


def get_execution_time(record):
    try:
        return float(record.get("execution_time", 0))
    except (TypeError, ValueError):
        return 0.0


def get_error_type(record):
    return (
        record.get("error_type")
        or record.get("exception_type")
        or record.get("exception")
        or record.get("error_name")
        or ""
    )


def is_valid_execution(record):
    # Direct boolean format
    if record.get("success") is True:
        return True

    if record.get("success") is False:
        return False

    # String status format
    status = str(record.get("status", "")).lower()
    if status in {"ok", "success", "successful", "valid", "passed", "pass"}:
        return True

    if status in {"error", "failed", "fail", "crash", "exception"}:
        return False

    # Some logs store result/output for successful execution
    if record.get("result") is not None and not get_error_type(record):
        return True

    if record.get("output") is not None and not get_error_type(record):
        return True

    # If there is an error message or error type, it is not valid
    if get_error_type(record):
        return False

    if record.get("error_message") or record.get("message"):
        return False

    # Last fallback: no error fields means valid
    return True


def summarize(records):
    total_inputs = len(records)
    valid_inputs = 0
    crash_error_inputs = 0
    error_types = Counter()
    execution_times = []
    input_values = []

    for record in records:
        input_values.append(get_input_value(record))
        execution_times.append(get_execution_time(record))

        if is_valid_execution(record):
            valid_inputs += 1
        else:
            crash_error_inputs += 1
            error_type = get_error_type(record) or "UnknownError"
            error_types[error_type] += 1

    unique_inputs = len(set(input_values))
    duplicate_inputs = total_inputs - unique_inputs

    average_execution_time = (
        sum(execution_times) / len(execution_times)
        if execution_times
        else 0.0
    )

    return {
        "total_inputs": total_inputs,
        "valid_inputs": valid_inputs,
        "crash_error_inputs": crash_error_inputs,
        "unique_inputs": unique_inputs,
        "duplicate_inputs": duplicate_inputs,
        "average_execution_time": average_execution_time,
        "error_types": dict(error_types),
    }


def print_summary(random_summary, ai_summary):
    print("\nWeek 7 Pilot Experiment Summary")
    print("--------------------------------")
    print(f"{'Metric':<28} {'Random':<15} {'AI-Guided':<15}")
    print("-" * 60)

    rows = [
        ("Total Inputs", "total_inputs"),
        ("Valid Inputs", "valid_inputs"),
        ("Crash/Error Inputs", "crash_error_inputs"),
        ("Unique Inputs", "unique_inputs"),
        ("Duplicate Inputs", "duplicate_inputs"),
        ("Avg Execution Time", "average_execution_time"),
    ]

    for label, key in rows:
        random_value = random_summary[key]
        ai_value = ai_summary[key]

        if key == "average_execution_time":
            random_value = f"{random_value:.8f}"
            ai_value = f"{ai_value:.8f}"

        print(f"{label:<28} {str(random_value):<15} {str(ai_value):<15}")

    print("\nRandom Error Types:")
    for error_type, count in random_summary["error_types"].items():
        print(f"- {error_type}: {count}")

    print("\nAI Error Types:")
    for error_type, count in ai_summary["error_types"].items():
        print(f"- {error_type}: {count}")


def save_summary(random_summary, ai_summary):
    output = {
        "random_pilot": random_summary,
        "ai_pilot": ai_summary,
    }

    path = Path(SUMMARY_OUTPUT_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"\nSummary saved to: {SUMMARY_OUTPUT_FILE}")


def main():
    random_records = load_jsonl(RANDOM_RESULTS_FILE)
    ai_records = load_jsonl(AI_RESULTS_FILE)

    random_summary = summarize(random_records)
    ai_summary = summarize(ai_records)

    print_summary(random_summary, ai_summary)
    save_summary(random_summary, ai_summary)


if __name__ == "__main__":
    main()