import random
import string


STRATEGY_NAME = "token_aware_random"

FILLER_CHARS = string.ascii_letters + string.digits


def random_filler(max_length=8):
    length = random.randint(0, max_length)
    return "".join(random.choice(FILLER_CHARS) for _ in range(length))


def generate_input(target, max_tokens=10):
    tokens = target.get("tokens", [])

    if not tokens:
        return random_filler(20)

    parts = []

    token_count = random.randint(1, max_tokens)

    for _ in range(token_count):
        choice_type = random.random()

        if choice_type < 0.65:
            parts.append(random.choice(tokens))
        elif choice_type < 0.85:
            parts.append(random_filler())
        else:
            parts.append(random.choice(["", " ", "\n", "\t"]))

    separator = random.choice(["", " ", "", "", "\n"])

    return separator.join(parts)


def generate_inputs(target, count=100):
    return [generate_input(target) for _ in range(count)]