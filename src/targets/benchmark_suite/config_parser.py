def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Config input cannot be empty")

    config = {}

    lines = input_string.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "=" not in line:
            raise ValueError("Config line must contain '='")

        if line.count("=") != 1:
            raise ValueError("Config line must contain exactly one '='")

        key, value = line.split("=")

        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError("Config key cannot be empty")

        if not value:
            raise ValueError("Config value cannot be empty")

        if key in config:
            raise ValueError("Duplicate config key")

        config[key] = value

    if not config:
        raise ValueError("No valid config entries found")

    return {
        "valid": True,
        "entries": config,
        "entry_count": len(config),
    }