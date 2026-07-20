def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    text = input_string.strip()

    if not text:
        raise ValueError("Protocol message cannot be empty")

    if text.startswith("AUTH:"):
        parts = text.split(":")

        if len(parts) != 3:
            raise ValueError("AUTH message must be AUTH:user:password")

        _, user, password = parts

        if not user or not password:
            raise ValueError("AUTH user and password cannot be empty")

        return {
            "valid": True,
            "type": "AUTH",
            "user": user,
        }

    if text.startswith("MSG|"):
        parts = text.split("|")

        if len(parts) != 3:
            raise ValueError("MSG message must be MSG|payload|END")

        command, payload, ending = parts

        if command != "MSG":
            raise ValueError("Invalid MSG command")

        if not payload:
            raise ValueError("MSG payload cannot be empty")

        if ending != "END":
            raise ValueError("MSG message must end with END")

        return {
            "valid": True,
            "type": "MSG",
            "payload_length": len(payload),
        }

    if text.startswith("DATA:"):
        payload = text.split(":", 1)[1]

        if not payload:
            raise ValueError("DATA payload cannot be empty")

        if not payload.isdigit():
            raise ValueError("DATA payload must be numeric")

        return {
            "valid": True,
            "type": "DATA",
            "value": int(payload),
        }

    raise ValueError("Unknown protocol message type")