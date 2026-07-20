import csv
import importlib
import inspect
import json
from collections import Counter, defaultdict
from pathlib import Path

from src.targets.benchmark_suite.target_registry import get_all_targets

RESULT_ROOT = Path("results/week8/random_baseline")
SUMMARY_JSON = RESULT_ROOT / "week8_random_summary.json"
SUMMARY_CSV = RESULT_ROOT / "week8_random_summary.csv"


def load_jsonl(file_path):
    records = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    return records


def load_module(module_path):
    return importlib.import_module(module_path)


def get_module_file(module):
    module_file = getattr(module, "__file__", None)

    if not module_file:
        return None

    return Path(module_file)


def count_module_code_lines(module_file):
    """
    Count non-empty, non-comment code lines in the whole target module.

    Previous bug:
    - covered_lines came from the whole target file
    - source_line_count came only from the main function
    That caused impossible coverage values over 100%.

    This fixes the denominator by using the whole target module.
    """
    if not module_file or not module_file.exists():
        return set()

    code_lines = set()

    with module_file.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                continue

            code_lines.add(line_number)

    return code_lines


def build_target_metadata():
    metadata = {}

    for target in get_all_targets():
        module = load_module(target["module"])
        module_file = get_module_file(module)
        module_code_lines = count_module_code_lines(module_file)

        metadata[target["name"]] = {
            "module": target["module"],
            "function": target["function"],
            "module_file": str(module_file) if module_file else None,
            "module_code_lines": module_code_lines,
            "module_code_line_count": len(module_code_lines),
        }

    return metadata


def summarize_result_file(file_path, target_metadata):
    records = load_jsonl(file_path)

    if not records:
        return None

    first = records[0]
    target_name = first.get("target_name")

    total_inputs = len(records)
    valid_inputs = sum(1 for record in records if record.get("success") is True)
    crash_error_inputs = total_inputs - valid_inputs

    input_values = [record.get("input", "") for record in records]
    unique_inputs = len(set(input_values))
    duplicate_inputs = total_inputs - unique_inputs

    execution_times = [
        float(record.get("execution_time", 0.0))
        for record in records
    ]

    average_execution_time = (
        sum(execution_times) / len(execution_times)
        if execution_times
        else 0.0
    )

    error_counter = Counter()

    for record in records:
        if record.get("success") is False:
            error_type = record.get("error_type") or "UnknownError"
            error_counter[error_type] += 1

    covered_lines = set()

    for record in records:
        for line_number in record.get("covered_lines", []):
            covered_lines.add(line_number)

    metadata = target_metadata.get(target_name, {})
    module_code_lines = metadata.get("module_code_lines", set())

    # Use the whole module denominator, plus any observed covered line just in case
    # tracing observed a valid line that our simple source-line scan did not count.
    coverage_denominator_lines = set(module_code_lines)
    coverage_denominator_lines.update(covered_lines)

    source_line_count = len(coverage_denominator_lines)
    covered_line_count = len(covered_lines)

    coverage_percent = 0.0

    if source_line_count:
        coverage_percent = covered_line_count / source_line_count * 100

    return {
        "target_name": first.get("target_name"),
        "target_difficulty": first.get("target_difficulty"),
        "target_category": first.get("target_category"),
        "strategy_name": first.get("strategy_name"),
        "trial_number": first.get("trial_number"),
        "total_inputs": total_inputs,
        "valid_inputs": valid_inputs,
        "crash_error_inputs": crash_error_inputs,
        "unique_inputs": unique_inputs,
        "duplicate_inputs": duplicate_inputs,
        "average_execution_time": average_execution_time,
        "coverage_percent": coverage_percent,
        "covered_line_count": covered_line_count,
        "source_line_count": source_line_count,
        "unique_error_type_count": len(error_counter),
        "error_types": dict(error_counter),
        "result_file": str(file_path),
    }


def average(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def aggregate_by_key(rows, key):
    grouped = defaultdict(list)

    for row in rows:
        grouped[row[key]].append(row)

    summary = {}

    for group_name, group_rows in grouped.items():
        summary[group_name] = {
            "experiment_groups": len(group_rows),
            "total_inputs": sum(row["total_inputs"] for row in group_rows),
            "valid_inputs": sum(row["valid_inputs"] for row in group_rows),
            "crash_error_inputs": sum(row["crash_error_inputs"] for row in group_rows),
            "average_valid_rate": average(
                row["valid_inputs"] / row["total_inputs"]
                for row in group_rows
                if row["total_inputs"]
            ),
            "average_error_rate": average(
                row["crash_error_inputs"] / row["total_inputs"]
                for row in group_rows
                if row["total_inputs"]
            ),
            "average_coverage_percent": average(
                row["coverage_percent"]
                for row in group_rows
            ),
            "average_execution_time": average(
                row["average_execution_time"]
                for row in group_rows
            ),
        }

    return summary


def write_csv(rows):
    fieldnames = [
        "target_name",
        "target_difficulty",
        "target_category",
        "strategy_name",
        "trial_number",
        "total_inputs",
        "valid_inputs",
        "crash_error_inputs",
        "unique_inputs",
        "duplicate_inputs",
        "average_execution_time",
        "coverage_percent",
        "covered_line_count",
        "source_line_count",
        "unique_error_type_count",
        "error_types",
        "result_file",
    ]

    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            csv_row = row.copy()
            csv_row["error_types"] = json.dumps(csv_row["error_types"])
            writer.writerow(csv_row)


def write_json(rows):
    coverage_over_100_groups = [
        row
        for row in rows
        if row["coverage_percent"] > 100.0
    ]

    output = {
        "total_experiment_groups": len(rows),
        "total_inputs": sum(row["total_inputs"] for row in rows),
        "overall_valid_inputs": sum(row["valid_inputs"] for row in rows),
        "overall_crash_error_inputs": sum(row["crash_error_inputs"] for row in rows),
        "overall_valid_rate": (
            sum(row["valid_inputs"] for row in rows)
            / sum(row["total_inputs"] for row in rows)
        ),
        "overall_error_rate": (
            sum(row["crash_error_inputs"] for row in rows)
            / sum(row["total_inputs"] for row in rows)
        ),
        "coverage_over_100_group_count": len(coverage_over_100_groups),
        "by_difficulty": aggregate_by_key(rows, "target_difficulty"),
        "by_strategy": aggregate_by_key(rows, "strategy_name"),
        "by_target": aggregate_by_key(rows, "target_name"),
        "rows": rows,
    }

    with SUMMARY_JSON.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)


def print_summary(rows):
    total_inputs = sum(row["total_inputs"] for row in rows)
    total_valid = sum(row["valid_inputs"] for row in rows)
    total_errors = sum(row["crash_error_inputs"] for row in rows)

    max_coverage = max(row["coverage_percent"] for row in rows)
    coverage_over_100 = sum(1 for row in rows if row["coverage_percent"] > 100.0)

    print("\nWeek 8 Random Baseline Summary")
    print("------------------------------")
    print(f"Experiment groups: {len(rows)}")
    print(f"Total inputs: {total_inputs}")
    print(f"Valid inputs: {total_valid}")
    print(f"Crash/error inputs: {total_errors}")
    print(f"Overall valid rate: {total_valid / total_inputs * 100:.2f}%")
    print(f"Overall error rate: {total_errors / total_inputs * 100:.2f}%")
    print(f"Max coverage percent: {max_coverage:.2f}%")
    print(f"Coverage groups over 100%: {coverage_over_100}")

    print("\nBy Strategy")
    print("-----------")

    by_strategy = aggregate_by_key(rows, "strategy_name")

    for strategy_name, data in by_strategy.items():
        print(
            f"{strategy_name}: "
            f"groups={data['experiment_groups']}, "
            f"inputs={data['total_inputs']}, "
            f"valid={data['valid_inputs']}, "
            f"errors={data['crash_error_inputs']}, "
            f"avg_coverage={data['average_coverage_percent']:.2f}%"
        )

    print("\nBy Difficulty")
    print("-------------")

    by_difficulty = aggregate_by_key(rows, "target_difficulty")

    for difficulty, data in by_difficulty.items():
        print(
            f"{difficulty}: "
            f"groups={data['experiment_groups']}, "
            f"inputs={data['total_inputs']}, "
            f"valid={data['valid_inputs']}, "
            f"errors={data['crash_error_inputs']}, "
            f"avg_coverage={data['average_coverage_percent']:.2f}%"
        )

    print(f"\nSummary JSON saved to: {SUMMARY_JSON}")
    print(f"Summary CSV saved to: {SUMMARY_CSV}")


def main():
    result_files = sorted(RESULT_ROOT.glob("*/*.jsonl"))

    rows = []

    if not result_files:
        print(f"No result files found under: {RESULT_ROOT}")
        return

    target_metadata = build_target_metadata()

    for file_path in result_files:
        summary = summarize_result_file(file_path, target_metadata)

        if summary:
            rows.append(summary)

    if not rows:
        print(f"No readable result rows found under: {RESULT_ROOT}")
        return

    write_json(rows)
    write_csv(rows)
    print_summary(rows)


if __name__ == "__main__":
    main()