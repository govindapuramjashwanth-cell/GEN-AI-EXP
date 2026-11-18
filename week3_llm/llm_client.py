from abc import ABC, abstractmethod
import time
import requests
from google import genai
from google.genai import types
from cost_calculator import calculate_cost

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt):
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, api_key, model="gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=120000))
        self.model = model

    def generate(self, prompt):
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        usage = response.usage_metadata
        return {
            "response": response.text or "",
            "input_tokens": usage.prompt_token_count if usage else 0,
            "output_tokens": usage.candidates_token_count if usage else 0,
        }

class OllamaProvider(LLMProvider):
    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        response = requests.post(
            self.url,
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "response": data["response"],
            "input_tokens": data.get("prompt_eval_count", 0),
            "output_tokens": data.get("eval_count", 0),
        }

class LLMClient:
    def __init__(self, provider, logger):
        self.provider = provider
        self.logger = logger

    def generate(self, prompt):
        max_attempts = 3
        start = time.perf_counter()
        last_error = None
        attempt = 0
        for attempt in range(1, max_attempts + 1):
            try:
                result = self.provider.generate(prompt)
                latency = round((time.perf_counter() - start) * 1000, 2)
                input_tokens = result["input_tokens"]
                output_tokens = result["output_tokens"]
                provider_name = type(self.provider).__name__
                log_data = {
                    "provider": provider_name,
                    "model": self.provider.model,
                    "prompt": prompt,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "latency_ms": latency,
                    "cost": calculate_cost(provider_name, self.provider.model, input_tokens, output_tokens),
                    "attempts": attempt,
                    "status": "success",
                    "error": None,
                }
                try:
                    self.logger.log_call(log_data)
                except Exception as log_error:
                    print("MongoDB logging error:", log_error)
                return result["response"]
            except Exception as error:
                last_error = error
                code = getattr(error, "status_code", None)
                retryable = (
                    isinstance(error, (requests.exceptions.Timeout, requests.exceptions.ConnectionError))
                    or code == 429
                    or (isinstance(code, int) and code >= 500)
                    or (
                        isinstance(error, requests.exceptions.HTTPError)
                        and error.response is not None
                        and (error.response.status_code == 429 or error.response.status_code >= 500)
                    )
                )
                if not retryable or attempt == max_attempts:
                    break
                delay = 2 ** (attempt - 1)
                print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
                time.sleep(delay)

        latency = round((time.perf_counter() - start) * 1000, 2)
        failed_log = {
            "provider": type(self.provider).__name__,
            "model": self.provider.model,
            "prompt": prompt,
            "latency_ms": latency,
            "attempts": attempt,
            "status": "failed",
            "error": str(last_error),
        }
        try:
            self.logger.log_call(failed_log)
        except Exception as log_error:
            print("MongoDB logging error:", log_error)
        raise last_error
