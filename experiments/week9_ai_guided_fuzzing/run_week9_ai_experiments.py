import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from experiments.week8_random_baseline.run_week8_random_experiments import (
    execute_with_line_coverage,
    load_function,
    save_records,
)
from experiments.week8_random_baseline.summarize_week8_random_results import (
    build_target_metadata,
)
from src.fuzzers.ai_guided.ai_guided_fuzzer import generate_ai_inputs
from src.fuzzers.ai_guided.ai_model_registry import (
    get_ai_model_by_name,
    get_all_ai_models,
)
from src.fuzzers.ai_guided.mindrouter_client import MindRouterClient
from src.targets.benchmark_suite.target_registry import (
    get_all_targets,
    get_target_by_name,
)


OUTPUT_ROOT = Path("results/week9/ai_guided")
PROMPT_VERSION = "week9_target_aware_v1"

SMOKE_TARGETS = [
    "email_validator",
    "arithmetic_script_parser",
]

SMOKE_MODEL = "qwen_qwen3_5_122b"


def make_output_file(target_name, model_name, trial_number):
    target_directory = OUTPUT_ROOT / target_name
    target_directory.mkdir(parents=True, exist_ok=True)

    return target_directory / f"{model_name}_trial{trial_number}.jsonl"


def make_metadata_file(target_name, model_name, trial_number):
    target_directory = OUTPUT_ROOT / target_name
    target_directory.mkdir(parents=True, exist_ok=True)

    return target_directory / f"{model_name}_trial{trial_number}_metadata.json"


def write_json(data, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def calculate_coverage(covered_lines, module_code_lines):
    """
    Use the corrected Week 8 module-level denominator.

    The union protects against impossible coverage values above 100%
    if tracing observes a valid executable line not detected by the
    simple source scan.
    """
    covered_line_set = set(covered_lines)
    denominator_lines = set(module_code_lines)
    denominator_lines.update(covered_line_set)

    source_line_count = len(denominator_lines)
    covered_line_count = len(covered_line_set)

    coverage_percent = 0.0

    if source_line_count:
        coverage_percent = (
            covered_line_count / source_line_count * 100
        )

    return {
        "covered_line_count": covered_line_count,
        "source_line_count": source_line_count,
        "coverage_percent": coverage_percent,
    }


def run_single_experiment(
    target,
    model,
    trial_number,
    input_count,
    batch_size,
    client,
    target_metadata,
    overwrite=False,
):
    output_file = make_output_file(
        target_name=target["name"],
        model_name=model["name"],
        trial_number=trial_number,
    )

    metadata_file = make_metadata_file(
        target_name=target["name"],
        model_name=model["name"],
        trial_number=trial_number,
    )

    if output_file.exists() and not overwrite:
        print(
            f"[SKIP] target={target['name']} | "
            f"model={model['name']} | "
            f"trial={trial_number} | "
            f"reason=output already exists"
        )
        return "skipped"

    started_at = datetime.now(timezone.utc).isoformat()
    generation_start = time.perf_counter()

    try:
        generation_result = generate_ai_inputs(
            target=target,
            model_id=model["model_id"],
            count=input_count,
            trial_number=trial_number,
            batch_size=batch_size,
            client=client,
        )

    except Exception as error:
        generation_time = time.perf_counter() - generation_start

        failure_metadata = {
            "status": "generation_failed",
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "target_name": target["name"],
            "target_difficulty": target["difficulty"],
            "target_category": target["category"],
            "model_name": model["name"],
            "model_id": model["model_id"],
            "provider": model["provider"],
            "trial_number": trial_number,
            "requested_input_count": input_count,
            "batch_size": batch_size,
            "prompt_version": PROMPT_VERSION,
            "generation_time": generation_time,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }

        write_json(failure_metadata, metadata_file)

        print(
            f"[FAIL] target={target['name']} | "
            f"model={model['name']} | "
            f"trial={trial_number} | "
            f"error={type(error).__name__}: {error}"
        )

        return "failed"

    generation_time = time.perf_counter() - generation_start
    generated_inputs = generation_result["generated_inputs"]

    target_function = load_function(
        target["module"],
        target["function"],
    )

    module_code_lines = target_metadata[target["name"]][
        "module_code_lines"
    ]

    records = []

    for input_index, input_value in enumerate(
        generated_inputs,
        start=1,
    ):
        execution = execute_with_line_coverage(
            target=target,
            target_function=target_function,
            input_value=input_value,
        )

        coverage = calculate_coverage(
            covered_lines=execution["covered_lines"],
            module_code_lines=module_code_lines,
        )

        record = {
            "target_name": target["name"],
            "target_difficulty": target["difficulty"],
            "target_category": target["category"],
            "fuzzer_type": "ai_guided",
            "strategy_name": model["name"],
            "model_name": model["name"],
            "model_id": model["model_id"],
            "provider": model["provider"],
            "prompt_version": PROMPT_VERSION,
            "trial_number": trial_number,
            "input_index": input_index,
            "input": input_value,
            "success": execution["success"],
            "result": execution["result"],
            "error_type": execution["error_type"],
            "error_message": execution["error_message"],
            "execution_time": execution["execution_time"],
            "covered_lines": execution["covered_lines"],
            "coverage_count": coverage["covered_line_count"],
            "source_line_count": coverage["source_line_count"],
            "coverage_percent": coverage["coverage_percent"],
            "generation_time_total": generation_time,
            "generation_time_per_input": (
                generation_time / len(generated_inputs)
                if generated_inputs
                else 0.0
            ),
            "generation_rounds": generation_result[
                "generation_rounds"
            ],
            "raw_response_count": generation_result[
                "raw_response_count"
            ],
        }

        records.append(record)

    save_records(records, output_file)

    valid_count = sum(
        1 for record in records
        if record["success"] is True
    )
    error_count = len(records) - valid_count

    experiment_metadata = {
        "status": "completed",
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "target_name": target["name"],
        "target_difficulty": target["difficulty"],
        "target_category": target["category"],
        "model_name": model["name"],
        "model_id": model["model_id"],
        "provider": model["provider"],
        "trial_number": trial_number,
        "requested_input_count": input_count,
        "completed_input_count": len(records),
        "valid_input_count": valid_count,
        "crash_error_input_count": error_count,
        "batch_size": batch_size,
        "prompt_version": PROMPT_VERSION,
        "generation_time": generation_time,
        "generation_rounds": generation_result[
            "generation_rounds"
        ],
        "raw_response_count": generation_result[
            "raw_response_count"
        ],
        "rejected_inputs": generation_result[
            "rejected_inputs"
        ],
        "generation_errors": generation_result[
            "generation_errors"
        ],
        "result_file": str(output_file),
    }

    write_json(experiment_metadata, metadata_file)

    print(
        f"[DONE] target={target['name']} | "
        f"model={model['name']} | "
        f"trial={trial_number} | "
        f"inputs={len(records)} | "
        f"valid={valid_count} | "
        f"errors={error_count} | "
        f"generation_time={generation_time:.2f}s"
    )

    return "completed"


def select_targets(target_names=None):
    if not target_names:
        return get_all_targets()

    return [
        get_target_by_name(target_name)
        for target_name in target_names
    ]


def select_models(model_names=None):
    if not model_names:
        return get_all_ai_models()

    return [
        get_ai_model_by_name(model_name)
        for model_name in model_names
    ]


def run_all_experiments(
    input_count,
    trials,
    batch_size,
    target_names=None,
    model_names=None,
    overwrite=False,
):
    targets = select_targets(target_names)
    models = select_models(model_names)
    target_metadata = build_target_metadata()
    client = MindRouterClient()

    total_groups = len(targets) * len(models) * trials

    print("\nWeek 9 AI-Guided Fuzzing")
    print("------------------------")
    print(f"Targets: {len(targets)}")
    print(f"Models: {len(models)}")
    print(f"Trials: {trials}")
    print(f"Inputs per group: {input_count}")
    print(f"Total experiment groups: {total_groups}")
    print(
        f"Planned target executions: "
        f"{total_groups * input_count}"
    )
    print(f"Output root: {OUTPUT_ROOT}\n")

    status_counts = {
        "completed": 0,
        "skipped": 0,
        "failed": 0,
    }

    current_group = 0

    for target in targets:
        for model in models:
            for trial_number in range(1, trials + 1):
                current_group += 1

                print(
                    f"[START {current_group}/{total_groups}] "
                    f"target={target['name']} | "
                    f"model={model['name']} | "
                    f"trial={trial_number}"
                )

                status = run_single_experiment(
                    target=target,
                    model=model,
                    trial_number=trial_number,
                    input_count=input_count,
                    batch_size=batch_size,
                    client=client,
                    target_metadata=target_metadata,
                    overwrite=overwrite,
                )

                status_counts[status] += 1

    print("\nWeek 9 run finished")
    print("-------------------")
    print(f"Completed groups: {status_counts['completed']}")
    print(f"Skipped groups: {status_counts['skipped']}")
    print(f"Failed groups: {status_counts['failed']}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run Week 9 AI-guided fuzzing experiments."
    )

    parser.add_argument(
        "--input-count",
        type=int,
        default=500,
        help="Inputs generated per target, model, and trial.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=3,
        help="Number of trials per target and model.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Inputs requested in each MindRouter generation call.",
    )

    parser.add_argument(
        "--targets",
        nargs="*",
        help="Optional target names from the target registry.",
    )

    parser.add_argument(
        "--models",
        nargs="*",
        help="Optional model names from the AI model registry.",
    )

    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run 2 targets, 1 model, 10 inputs, and 1 trial.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing experiment result files.",
    )

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    if arguments.smoke:
        run_all_experiments(
            input_count=10,
            trials=1,
            batch_size=10,
            target_names=SMOKE_TARGETS,
            model_names=[SMOKE_MODEL],
            overwrite=arguments.overwrite,
        )
        return

    run_all_experiments(
        input_count=arguments.input_count,
        trials=arguments.trials,
        batch_size=arguments.batch_size,
        target_names=arguments.targets,
        model_names=arguments.models,
        overwrite=arguments.overwrite,
    )


if __name__ == "__main__":
    main()
