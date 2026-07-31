from src.fuzzers.ai_guided.ai_input_validator import filter_ai_inputs
from src.fuzzers.ai_guided.ai_prompt_builder import build_generation_prompt
from src.fuzzers.ai_guided.ai_response_parser import parse_generated_inputs
from src.fuzzers.ai_guided.mindrouter_client import MindRouterClient


DEFAULT_BATCH_SIZE = 20
DEFAULT_MAX_INPUT_LENGTH = 500


def generate_ai_inputs(
    target,
    model_id,
    count=100,
    trial_number=1,
    batch_size=DEFAULT_BATCH_SIZE,
    max_input_length=DEFAULT_MAX_INPUT_LENGTH,
    temperature=0.8,
    max_rounds=None,
    client=None,
):
    """
    Generate unique and validated AI-guided inputs for one target.
    """
    if count <= 0:
        raise ValueError("count must be greater than zero.")

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero.")

    client = client or MindRouterClient()

    if max_rounds is None:
        expected_batches = (count + batch_size - 1) // batch_size
        max_rounds = max(expected_batches * 6, 20)

    accepted_inputs = []
    accepted_set = set()
    rejected_inputs = []
    generation_errors = []

    raw_response_count = 0
    duplicate_input_count = 0
    round_number = 0

    while len(accepted_inputs) < count and round_number < max_rounds:
        round_number += 1

        remaining = count - len(accepted_inputs)
        requested_batch_size = min(batch_size, remaining)

        system_prompt, user_prompt = build_generation_prompt(
            target=target,
            input_count=requested_batch_size,
            max_input_length=max_input_length,
            trial_number=trial_number,
            round_number=round_number,
            existing_inputs=accepted_inputs,
        )

        try:
            response_text = client.generate_text(
                model=model_id,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=6000,
                json_mode=False,
            )

            raw_response_count += 1

            parsed_inputs = parse_generated_inputs(
                response_text=response_text,
                expected_count=None,
                max_input_length=max_input_length,
            )

            safe_inputs, rejected = filter_ai_inputs(
                target_name=target["name"],
                inputs=parsed_inputs,
            )

            rejected_inputs.extend(rejected)

            added_this_round = 0

            for value in safe_inputs:
                if value in accepted_set:
                    duplicate_input_count += 1
                    continue

                accepted_set.add(value)
                accepted_inputs.append(value)
                added_this_round += 1

                if len(accepted_inputs) >= count:
                    break

            if added_this_round == 0:
                generation_errors.append({
                    "round_number": round_number,
                    "error_type": "NoNewUniqueInputs",
                    "error_message": (
                        "The response produced no new accepted unique inputs."
                    ),
                })

        except Exception as error:
            generation_errors.append({
                "round_number": round_number,
                "error_type": type(error).__name__,
                "error_message": str(error),
            })

    if len(accepted_inputs) < count:
        raise RuntimeError(
            f"AI generation stopped after {round_number} rounds. "
            f"Requested {count} unique inputs but collected "
            f"{len(accepted_inputs)}. "
            f"Duplicate inputs encountered: {duplicate_input_count}. "
            f"Errors: {generation_errors}"
        )

    return {
        "target_name": target["name"],
        "model_id": model_id,
        "trial_number": trial_number,
        "requested_input_count": count,
        "generated_inputs": accepted_inputs[:count],
        "unique_input_count": len(accepted_inputs[:count]),
        "generation_rounds": round_number,
        "raw_response_count": raw_response_count,
        "duplicate_input_count": duplicate_input_count,
        "rejected_inputs": rejected_inputs,
        "generation_errors": generation_errors,
    }