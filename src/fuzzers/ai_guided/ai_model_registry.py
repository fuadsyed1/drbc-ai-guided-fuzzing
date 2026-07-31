AI_MODELS = [
    {
        "name": "qwen_qwen3_5_122b",
        "model_id": "qwen/qwen3.5-122b",
        "provider": "mindrouter",
        "description": "Large Qwen model used as the main AI-guided fuzzing model.",
    },
    {
        "name": "openai_gpt_oss_120b",
        "model_id": "openai/gpt-oss-120b",
        "provider": "mindrouter",
        "description": "Large open-weight GPT-OSS model used as a different model-family comparison.",
    },
    {
        "name": "qwen_qwen3_6_35b",
        "model_id": "qwen/qwen3.6-35b",
        "provider": "mindrouter",
        "description": "Qwen 3.6 35B model used as the third AI-guided fuzzing comparison model.",
    },
    {
        "name": "google_gemma_4_31b",
        "model_id": "google/gemma-4-31b",
        "provider": "mindrouter",
        "description": "Gemma-family model used for model diversity.",
    },
]


def get_all_ai_models():
    return AI_MODELS


def get_ai_model_by_name(name):
    for model in AI_MODELS:
        if model["name"] == name:
            return model

    raise ValueError(f"Unknown AI model name: {name}")


def get_ai_model_names():
    return [model["name"] for model in AI_MODELS]
