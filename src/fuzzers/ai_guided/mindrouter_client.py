import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv


load_dotenv()

DEFAULT_BASE_URL = "https://mindrouter.uidaho.edu/v1"


class MindRouterClient:
    def __init__(
        self,
        api_key=None,
        base_url=None,
        timeout_seconds=None,
        default_model=None,
    ):
        self.api_key = (
            api_key
            or os.environ.get("LLM_API_KEY")
            or os.environ.get("MINDROUTER_API_KEY")
        )

        self.base_url = (
            base_url
            or os.environ.get("LLM_BASE_URL")
            or os.environ.get("MINDROUTER_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")

        self.default_model = (
            default_model
            or os.environ.get("LLM_MODEL_NAME")
        )

        self.timeout_seconds = int(
            timeout_seconds
            or os.environ.get("LLM_TIMEOUT_SECONDS", "180")
        )

        if not self.api_key:
            raise ValueError(
                "Missing API key. Add LLM_API_KEY to the local .env file."
            )

    def chat_completion(
        self,
        messages,
        model=None,
        temperature=0.2,
        max_tokens=1200,
        response_format=None,
    ):
        selected_model = model or self.default_model

        if not selected_model:
            raise ValueError(
                "Missing model name. Provide model or set LLM_MODEL_NAME."
            )

        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        if response_format is not None:
            payload["response_format"] = response_format

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)

        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"MindRouter HTTP error {error.code}: {body}"
            ) from error

        except urllib.error.URLError as error:
            raise RuntimeError(
                f"MindRouter connection error: {error}"
            ) from error

    def generate_text(
        self,
        system_prompt,
        user_prompt,
        model=None,
        temperature=0.2,
        max_tokens=1200,
        json_mode=False,
    ):
        response_format = {"type": "json_object"} if json_mode else None

        response = self.chat_completion(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
        )

        choices = response.get("choices", [])

        if not choices:
            raise RuntimeError(
                f"MindRouter response did not contain choices: {response}"
            )

        message = choices[0].get("message", {})
        content = message.get("content", "")

        if not content:
            raise RuntimeError(
                f"MindRouter response did not contain content: {response}"
            )

        return content