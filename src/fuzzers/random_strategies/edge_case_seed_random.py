import random
import string


STRATEGY_NAME = "edge_case_seed_random"

EXTRA_EDGE_CASES = [
    "",
    " ",
    "\n",
    "\t",
    "A" * 100,
    "0",
    "-1",
    "999999999999999999999",
    "null",
    "None",
    "undefined",
    "{}",
    "[]",
    "()",
    "<>",
    "::::",
    "////",
]


MUTATION_CHARS = string.ascii_letters + string.digits + string.punctuation + " "


def mutate_seed(seed):
    mutation_type = random.choice(
        [
            "return_original",
            "append_char",
            "prepend_char",
            "delete_char",
            "duplicate",
            "repeat",
            "wrap",
            "combine_with_noise",
        ]
    )

    if mutation_type == "return_original":
        return seed

    if mutation_type == "append_char":
        return seed + random.choice(MUTATION_CHARS)

    if mutation_type == "prepend_char":
        return random.choice(MUTATION_CHARS) + seed

    if mutation_type == "delete_char":
        if not seed:
            return seed
        index = random.randrange(len(seed))
        return seed[:index] + seed[index + 1:]

    if mutation_type == "duplicate":
        return seed + seed

    if mutation_type == "repeat":
        return seed * random.randint(1, 4)

    if mutation_type == "wrap":
        left, right = random.choice(
            [
                ("(", ")"),
                ("[", "]"),
                ("{", "}"),
                ("<", ">"),
                ("\"", "\""),
                ("'", "'"),
            ]
        )
        return left + seed + right

    if mutation_type == "combine_with_noise":
        noise = "".join(random.choice(MUTATION_CHARS) for _ in range(random.randint(1, 8)))
        return seed + noise

    return seed


def generate_input(target):
    target_edge_cases = target.get("edge_cases", [])
    target_seeds = target.get("seeds", [])

    seed_pool = target_edge_cases + target_seeds + EXTRA_EDGE_CASES

    if not seed_pool:
        seed_pool = EXTRA_EDGE_CASES

    seed = random.choice(seed_pool)
    return mutate_seed(seed)


def generate_inputs(target, count=100):
    return [generate_input(target) for _ in range(count)]