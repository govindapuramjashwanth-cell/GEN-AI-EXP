import os
from dotenv import load_dotenv
from llm_client import GeminiProvider, OllamaProvider, LLMClient
from mongo_logger import MongoLogger

load_dotenv()

def main():
    print("================================")
    print("       WEEK 3: LLM MONITORING")
    print("================================")
    print("1. Gemini")
    print("2. Ollama")
    choice = input("\nSelect provider (1/2): ").strip()
    logger = None
    try:
        logger = MongoLogger()
        if choice == "1":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API key not found in .env")
            provider = GeminiProvider(api_key, os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
        elif choice == "2":
            provider = OllamaProvider(os.getenv("OLLAMA_MODEL", "llama3.2"))
        else:
            raise ValueError("Invalid selection. Choose 1 or 2.")
        client = LLMClient(provider, logger)
        prompt = input("\nEnter your question: ").strip()
        if not prompt:
            raise ValueError("Please enter a question.")
        print("\n========== AI RESPONSE ==========")
        print(client.generate(prompt))
        print("\n========== COMPLETED ==========")
    except Exception as error:
        print("\nApplication error:", error)
    finally:
        if logger is not None:
            logger.close()

if __name__ == "__main__":
    main()
