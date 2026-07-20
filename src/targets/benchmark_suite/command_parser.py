import shlex


VALID_COMMANDS = {
    "run": {"min_args": 0, "max_args": 2, "flags": {"--verbose", "-v"}},
    "copy": {"min_args": 2, "max_args": 2, "flags": {"--force"}},
    "delete": {"min_args": 1, "max_args": 1, "flags": {"--force"}},
}


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Command cannot be empty")

    try:
        parts = shlex.split(input_string)
    except ValueError as error:
        raise ValueError(f"Invalid command syntax: {error}")

    if not parts:
        raise ValueError("Command cannot be empty")

    command = parts[0]

    if command not in VALID_COMMANDS:
        raise ValueError("Unknown command")

    spec = VALID_COMMANDS[command]
    flags = []
    args = []

    for part in parts[1:]:
        if part.startswith("-"):
            if part not in spec["flags"]:
                raise ValueError("Invalid flag for command")
            flags.append(part)
        else:
            args.append(part)

    if len(args) < spec["min_args"]:
        raise ValueError("Not enough command arguments")

    if len(args) > spec["max_args"]:
        raise ValueError("Too many command arguments")

    return {
        "valid": True,
        "command": command,
        "flags": flags,
        "args": args,
    }