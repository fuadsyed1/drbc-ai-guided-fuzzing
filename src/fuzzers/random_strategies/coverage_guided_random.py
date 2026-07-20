import importlib
import inspect
import random
import string
import sys
import time


STRATEGY_NAME = "coverage_guided_random"

MAX_SECONDS_PER_INPUT = 1.0
MAX_INPUT_LENGTH = 500
MAX_DIGIT_RUN_FOR_ARITHMETIC = 30

MUTATION_CHARS = string.ascii_letters + string.digits + string.punctuation + " \n\t"


def load_target_function(target):
    module = importlib.import_module(target["module"])
    return getattr(module, target["function"])


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


def is_safe_candidate(target, input_value):
    if not isinstance(input_value, str):
        return False

    if len(input_value) > MAX_INPUT_LENGTH:
        return False

    arithmetic_targets = {
        "calculator",
        "arithmetic_script_parser",
    }

    if target["name"] in arithmetic_targets:
        if "**" in input_value:
            return False

        if has_long_digit_run(input_value, MAX_DIGIT_RUN_FOR_ARITHMETIC):
            return False

    return True


def collect_line_coverage(target, target_function, input_value):
    if not is_safe_candidate(target, input_value):
        return set(), "SafetyError"

    covered_lines = set()
    target_file = inspect.getsourcefile(target_function)
    start_time = time.perf_counter()

    def trace_calls(frame, event, arg):
        elapsed = time.perf_counter() - start_time

        if elapsed > MAX_SECONDS_PER_INPUT:
            raise TimeoutError("Input execution timed out during coverage-guided generation")

        if event == "line" and frame.f_code.co_filename == target_file:
            covered_lines.add(frame.f_lineno)

        return trace_calls

    old_trace = sys.gettrace()
    sys.settrace(trace_calls)

    try:
        target_function(input_value)
        outcome = "success"
    except Exception as error:
        outcome = type(error).__name__
    finally:
        sys.settrace(old_trace)

    return covered_lines, outcome


def delete_random_char(value):
    if not value:
        return value

    index = random.randrange(len(value))
    return value[:index] + value[index + 1:]


def insert_random_char(value):
    index = random.randint(0, len(value))
    char = random.choice(MUTATION_CHARS)
    return value[:index] + char + value[index:]


def replace_random_char(value):
    if not value:
        return random.choice(MUTATION_CHARS)

    index = random.randrange(len(value))
    char = random.choice(MUTATION_CHARS)
    return value[:index] + char + value[index + 1:]


def duplicate_random_slice(value):
    if not value:
        return value

    start = random.randrange(len(value))
    end = random.randint(start + 1, len(value))
    piece = value[start:end]

    insert_at = random.randint(0, len(value))
    return value[:insert_at] + piece + value[insert_at:]


def combine_with_token(value, target):
    tokens = target.get("tokens", [])

    if not tokens:
        return value

    token = random.choice(tokens)
    insert_at = random.randint(0, len(value))
    return value[:insert_at] + token + value[insert_at:]


def mutate_once(value, target):
    mutation_type = random.choice(
        [
            "delete",
            "insert",
            "replace",
            "duplicate",
            "token_insert",
        ]
    )

    if mutation_type == "delete":
        return delete_random_char(value)

    if mutation_type == "insert":
        return insert_random_char(value)

    if mutation_type == "replace":
        return replace_random_char(value)

    if mutation_type == "duplicate":
        return duplicate_random_slice(value)

    if mutation_type == "token_insert":
        return combine_with_token(value, target)

    return value


def mutate_value(value, target):
    mutation_rounds = random.randint(1, 5)

    for _ in range(mutation_rounds):
        value = mutate_once(value, target)

        if len(value) > MAX_INPUT_LENGTH:
            value = value[:MAX_INPUT_LENGTH]

    return value


def make_seed_pool(target):
    seed_pool = []

    seed_pool.extend(target.get("seeds", []))
    seed_pool.extend(target.get("edge_cases", []))
    seed_pool.extend(target.get("tokens", []))

    seed_pool.extend(
        [
            "",
            " ",
            "test",
            "123",
            "0",
            "-1",
            "null",
            "{}",
            "[]",
            "()",
        ]
    )

    return seed_pool


def generate_inputs(target, count=100):
    target_function = load_target_function(target)

    seed_pool = make_seed_pool(target)
    corpus = list(seed_pool)

    generated_inputs = []
    seen_inputs = set()

    global_coverage = set()
    discovered_outcomes = set()

    max_attempts = count * 50
    attempts = 0

    while len(generated_inputs) < count and attempts < max_attempts:
        attempts += 1

        base_input = random.choice(corpus)
        candidate = mutate_value(base_input, target)

        if candidate in seen_inputs:
            continue

        seen_inputs.add(candidate)

        covered_lines, outcome = collect_line_coverage(
            target=target,
            target_function=target_function,
            input_value=candidate,
        )

        new_lines = covered_lines - global_coverage
        new_outcome = outcome not in discovered_outcomes

        if new_lines or new_outcome or len(generated_inputs) < count // 2:
            generated_inputs.append(candidate)
            corpus.append(candidate)
            global_coverage.update(covered_lines)
            discovered_outcomes.add(outcome)

    while len(generated_inputs) < count:
        base_input = random.choice(seed_pool)
        candidate = mutate_value(base_input, target)

        if is_safe_candidate(target, candidate):
            generated_inputs.append(candidate)
        else:
            generated_inputs.append("")

    return generated_inputs[:count]