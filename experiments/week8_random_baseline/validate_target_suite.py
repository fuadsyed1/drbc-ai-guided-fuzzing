import importlib

from src.targets.benchmark_suite.target_registry import get_all_targets


def load_target_function(target):
    module = importlib.import_module(target["module"])
    return getattr(module, target["function"])


def validate_target(target):
    target_function = load_target_function(target)

    seed = target["seeds"][0]

    try:
        result = target_function(seed)
        return {
            "name": target["name"],
            "status": "PASS",
            "seed": seed,
            "result": result,
        }
    except Exception as error:
        return {
            "name": target["name"],
            "status": "FAIL",
            "seed": seed,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }


def main():
    targets = get_all_targets()

    print("Week 8 Target Suite Validation")
    print("------------------------------")
    print(f"Total targets: {len(targets)}\n")

    passed = 0
    failed = 0

    for target in targets:
        result = validate_target(target)

        if result["status"] == "PASS":
            passed += 1
            print(f"[PASS] {result['name']} | seed: {result['seed']}")
        else:
            failed += 1
            print(f"[FAIL] {result['name']} | seed: {result['seed']}")
            print(f"       {result['error_type']}: {result['error_message']}")

    print("\nValidation Summary")
    print("------------------")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()