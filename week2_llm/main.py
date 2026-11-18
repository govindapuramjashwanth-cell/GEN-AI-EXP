import os
from dotenv import load_dotenv

from llm_client import GeminiProvider, OllamaProvider, LLMClient

load_dotenv()

def main():
    print("=== LLM Client ===")
    provider_name = input("Choose provider (gemini/ollama): ").strip().lower()

    if provider_name == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY is missing. Add it to your .env file.")
            return
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        provider = GeminiProvider(api_key, model=model)

    elif provider_name == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        provider = OllamaProvider(model=model)

    else:
        print("Invalid choice. Please enter gemini or ollama.")
        return

    prompt = input("Enter your question: ").strip()
    if not prompt:
        print("Please enter a question.")
        return

    client = LLMClient(provider)

    try:
        answer = client.generate(prompt)
        print("\nLLM Response:")
        print(answer)
    except Exception as error:
        print(f"\nRequest failed: {error}")

if __name__ == "__main__":
    main()
