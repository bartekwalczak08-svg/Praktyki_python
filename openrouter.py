import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_openrouter(prompt: str, model: str = "openai/gpt-3.5-turbo") -> str:
    """
    Wysyła zapytanie do OpenRouter API i zwraca odpowiedź modelu.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("Brak klucza OPENROUTER_API_KEY w zmiennych środowiskowych.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    pytanie = "Powiedz mi krótko czym jest OpenRouter."
    print(f"Pytanie: {pytanie}\n")
    odpowiedz = ask_openrouter(pytanie)
    print(f"Odpowiedź: {odpowiedz}")
