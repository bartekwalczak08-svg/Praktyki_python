import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_openrouter(
    prompt: str,
    conversation_history: list[dict[str, str]],
    model: str = "openai/gpt-3.5-turbo",
) -> str:
    """
    Wysyła zapytanie do OpenRouter API i zwraca odpowiedź modelu.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("Brak klucza OPENROUTER_API_KEY w zmiennych środowiskowych.")

    # Najpierw zapisujemy wiadomość użytkownika do historii.
    conversation_history.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": conversation_history,
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    assistant_reply = data["choices"][0]["message"]["content"]

    # Po odpowiedzi modelu dopisujemy rolę assistant do historii.
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


if __name__ == "__main__":
    conversation_history: list[dict[str, str]] = []

    pytanie_1 = "Powiedz mi krótko czym jest OpenRouter."
    print(f"Pytanie 1: {pytanie_1}\n")
    odpowiedz_1 = ask_openrouter(pytanie_1, conversation_history)
    print(f"Odpowiedź 1: {odpowiedz_1}\n")

    pytanie_2 = "Podaj teraz 3 praktyczne zastosowania."
    print(f"Pytanie 2: {pytanie_2}\n")
    odpowiedz_2 = ask_openrouter(pytanie_2, conversation_history)
    print(f"Odpowiedź 2: {odpowiedz_2}\n")

    print(f"Liczba wpisów w conversation_history: {len(conversation_history)}")
