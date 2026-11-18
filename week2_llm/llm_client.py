from abc import ABC, abstractmethod

import requests
from google import genai


class LLMProvider(ABC):
    """Common interface for all language-model providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class GeminiProvider(LLMProvider):
    """Cloud-based Gemini provider."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text or ""


class OllamaProvider(LLMProvider):
    """Local Ollama provider. Ollama must be installed and running."""

    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]


class LLMClient:
    """Uses the selected provider through one common interface."""

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)
