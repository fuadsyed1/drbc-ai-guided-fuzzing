import random
import string


STRATEGY_NAME = "mutation_based_random"

MUTATION_CHARS = string.ascii_letters + string.digits + string.punctuation + " "


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


def swap_two_chars(value):
    if len(value) < 2:
        return value

    chars = list(value)
    i, j = random.sample(range(len(chars)), 2)
    chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def truncate_value(value):
    if not value:
        return value

    end = random.randint(0, len(value))
    return value[:end]


def mutate_once(value):
    mutation = random.choice(
        [
            delete_random_char,
            insert_random_char,
            replace_random_char,
            duplicate_random_slice,
            swap_two_chars,
            truncate_value,
        ]
    )

    return mutation(value)


def generate_input(target):
    seeds = target.get("seeds", [])

    if not seeds:
        seeds = ["test", "123", "example"]

    value = random.choice(seeds)

    mutation_rounds = random.randint(1, 5)

    for _ in range(mutation_rounds):
        value = mutate_once(value)

    return value


def generate_inputs(target, count=100):
    return [generate_input(target) for _ in range(count)]