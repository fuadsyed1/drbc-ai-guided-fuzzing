RANDOM_STRATEGIES = [
    {
        "name": "basic_character_random",
        "module": "src.fuzzers.random_strategies.basic_character_random",
        "function": "generate_inputs",
        "description": "Pure random character generation baseline.",
    },
    {
        "name": "token_aware_random",
        "module": "src.fuzzers.random_strategies.token_aware_random",
        "function": "generate_inputs",
        "description": "Random generation using target-specific tokens.",
    },
    {
        "name": "edge_case_seed_random",
        "module": "src.fuzzers.random_strategies.edge_case_seed_random",
        "function": "generate_inputs",
        "description": "Random generation using known target edge cases and mutations.",
    },
    {
        "name": "mutation_based_random",
        "module": "src.fuzzers.random_strategies.mutation_based_random",
        "function": "generate_inputs",
        "description": "Random mutation of valid seed inputs.",
    },
    {
        "name": "coverage_guided_random",
        "module": "src.fuzzers.random_strategies.coverage_guided_random",
        "function": "generate_inputs",
        "description": "Simplified AFL-style coverage-guided random mutation.",
    },
]


def get_all_strategies():
    return RANDOM_STRATEGIES


def get_strategy_by_name(name):
    for strategy in RANDOM_STRATEGIES:
        if strategy["name"] == name:
            return strategy

    raise ValueError(f"Unknown random strategy: {name}")


def get_strategy_names():
    return [strategy["name"] for strategy in RANDOM_STRATEGIES]