import argparse
import importlib
import inspect
import json
import random
import sys
import time
from pathlib import Path

from src.targets.benchmark_suite.target_registry import get_all_targets
from src.fuzzers.random_strategies.strategy_registry import get_all_strategies

DEFAULT_INPUTS_PER_RUN = 100
DEFAULT_TRIALS = 3

MAX_SECONDS_PER_INPUT = 1.0
MAX_INPUT_LENGTH = 500
MAX_DIGIT_RUN_FOR_ARITHMETIC = 30

OUTPUT_ROOT = Path("results/week8/random_baseline")


def load_function(module_path, function_name):
    module = importlib.import_module(module_path)
    return getattr(module, function_name)


def safe_to_string(value):
    try:
        return repr(value)
    except Exception:
        return "<unrepresentable result>"


def count_source_lines(target_function):
    try:
        source_lines, _ = inspect.getsourcelines(target_function)
        return len(
            [
                line
                for line in source_lines
                if line.strip() and not line.strip().startswith("#")
            ]
        )
    except OSError:
        return 0


def has_long_digit_run(input_value, max_digits):
    current_run = 0

    for char in input_value:
        if char.isdigit():
            current_run += 1

            if current_run > max_digits:
                return True
        else:
            current_run = 0

    return False


def check_input_safety(target, input_value):
    if not isinstance(input_value, str):
        return False, "SafetyError", "Generated input is not a string"

    if len(input_value) > MAX_INPUT_LENGTH:
        return False, "SafetyError", "Generated input exceeded maximum length"

    arithmetic_targets = {
        "calculator",
        "arithmetic_script_parser",
    }

    if target["name"] in arithmetic_targets:
        if "**" in input_value:
            return False, "SafetyError", "Exponentiation is disabled for fuzzing safety"

        if has_long_digit_run(input_value, MAX_DIGIT_RUN_FOR_ARITHMETIC):
            return False, "SafetyError", "Numeric literal is too large for safe execution"

    return True, None, None


def safety_rejection_result(error_type, error_message):
    return {
        "success": False,
        "result": None,
        "error_type": error_type,
        "error_message": error_message,
        "execution_time": 0.0,
        "covered_lines": [],
        "coverage_count": 0,
    }


def execute_with_line_coverage(target, target_function, input_value):
    is_safe, error_type, error_message = check_input_safety(target, input_value)

    if not is_safe:
        return safety_rejection_result(error_type, error_message)

    covered_lines = set()
    target_file = inspect.getsourcefile(target_function)
    start_time = time.perf_counter()

    def trace_lines(frame, event, arg):
        elapsed = time.perf_counter() - start_time

        if elapsed > MAX_SECONDS_PER_INPUT:
            raise TimeoutError("Input execution timed out")

        if event == "line" and frame.f_code.co_filename == target_file:
            covered_lines.add(frame.f_lineno)

        return trace_lines

    old_trace = sys.gettrace()
    sys.settrace(trace_lines)

    try:
        result = target_function(input_value)
        execution_time = time.perf_counter() - start_time

        return {
            "success": True,
            "result": safe_to_string(result),
            "error_type": None,
            "error_message": None,
            "execution_time": execution_time,
            "covered_lines": sorted(covered_lines),
            "coverage_count": len(covered_lines),
        }

    except Exception as error:
        execution_time = time.perf_counter() - start_time

        return {
            "success": False,
            "result": None,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "execution_time": execution_time,
            "covered_lines": sorted(covered_lines),
            "coverage_count": len(covered_lines),
        }

    finally:
        sys.settrace(old_trace)


def make_output_file(target_name, strategy_name, trial_number):
    target_dir = OUTPUT_ROOT / target_name
    target_dir.mkdir(parents=True, exist_ok=True)

    return target_dir / f"{strategy_name}_trial{trial_number}.jsonl"


def save_records(records, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")


def run_single_experiment(target, strategy, trial_number, input_count):
    target_function = load_function(target["module"], target["function"])
    strategy_function = load_function(strategy["module"], strategy["function"])

    source_line_count = count_source_lines(target_function)

    experiment_seed = f"{target['name']}::{strategy['name']}::trial{trial_number}"
    random.seed(experiment_seed)

    generated_inputs = strategy_function(target, input_count)

    records = []

    for index, input_value in enumerate(generated_inputs, start=1):
        execution = execute_with_line_coverage(
            target=target,
            target_function=target_function,
            input_value=input_value,
        )

        coverage_percent = 0.0

        if source_line_count:
            coverage_percent = execution["coverage_count"] / source_line_count * 100

        record = {
            "target_name": target["name"],
            "target_difficulty": target["difficulty"],
            "target_category": target["category"],
            "strategy_name": strategy["name"],
            "trial_number": trial_number,
            "input_index": index,
            "input": input_value,
            "success": execution["success"],
            "result": execution["result"],
            "error_type": execution["error_type"],
            "error_message": execution["error_message"],
            "execution_time": execution["execution_time"],
            "covered_lines": execution["covered_lines"],
            "coverage_count": execution["coverage_count"],
            "source_line_count": source_line_count,
            "coverage_percent": coverage_percent,
        }

        records.append(record)

    output_file = make_output_file(
        target_name=target["name"],
        strategy_name=strategy["name"],
        trial_number=trial_number,
    )

    save_records(records, output_file)

    valid_count = sum(1 for record in records if record["success"])
    error_count = len(records) - valid_count

    print(
        f"[DONE] target={target['name']} | "
        f"strategy={strategy['name']} | "
        f"trial={trial_number} | "
        f"inputs={len(records)} | "
        f"valid={valid_count} | "
        f"errors={error_count}"
    )


def run_all_experiments(input_count, trials, limit_targets=None, limit_strategies=None):
    targets = get_all_targets()
    strategies = get_all_strategies()

    if limit_targets is not None:
        targets = targets[:limit_targets]

    if limit_strategies is not None:
        strategies = strategies[:limit_strategies]

    total_groups = len(targets) * len(strategies) * trials

    print("Week 8 Full Random Fuzzing Experiments")
    print("--------------------------------------")
    print(f"Targets: {len(targets)}")
    print(f"Strategies: {len(strategies)}")
    print(f"Trials: {trials}")
    print(f"Inputs per group: {input_count}")
    print(f"Experiment groups: {total_groups}")
    print(f"Total executions: {total_groups * input_count}")
    print(f"Max seconds per input: {MAX_SECONDS_PER_INPUT}")
    print("--------------------------------------")

    group_number = 0

    for target in targets:
        for strategy in strategies:
            for trial_number in range(1, trials + 1):
                group_number += 1

                print(
                    f"\n[{group_number}/{total_groups}] "
                    f"Running target={target['name']} | "
                    f"strategy={strategy['name']} | "
                    f"trial={trial_number}"
                )

                run_single_experiment(
                    target=target,
                    strategy=strategy,
                    trial_number=trial_number,
                    input_count=input_count,
                )

    print("\nAll Week 8 random baseline experiments completed.")
    print(f"Results saved under: {OUTPUT_ROOT}")


def main():
    parser = argparse.ArgumentParser(
        description="Run Week 8 random fuzzing baseline experiments."
    )

    parser.add_argument(
        "--inputs",
        type=int,
        default=DEFAULT_INPUTS_PER_RUN,
        help="Number of inputs per target/strategy/trial.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=DEFAULT_TRIALS,
        help="Number of repeated trials.",
    )

    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a small smoke test instead of the full experiment.",
    )

    args = parser.parse_args()

    if args.smoke:
        run_all_experiments(
            input_count=5,
            trials=1,
            limit_targets=2,
            limit_strategies=2,
        )
    else:
        run_all_experiments(
            input_count=args.inputs,
            trials=args.trials,
        )


if __name__ == "__main__":
    main()