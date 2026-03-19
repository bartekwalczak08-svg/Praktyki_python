import os
import requests
from dotenv import load_dotenv
from typing import Union

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

FewShotExample = tuple[str, str]  # (input, output)


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
    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    total_tokens = usage.get("total_tokens")

    if usage:
        print(
            "Tokeny -> "
            f"prompt: {prompt_tokens}, "
            f"completion: {completion_tokens}, "
            f"total: {total_tokens}"
        )
    else:
        print("Tokeny -> brak danych usage od providera/modelu")

    assistant_reply = data["choices"][0]["message"]["content"]

    # Po odpowiedzi modelu dopisujemy rolę assistant do historii.
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


def build_few_shot_prompt(
    task_description: str,
    examples: list[FewShotExample],
    user_input: str,
    example_separator: str = "\n---\n"
) -> str:
    """
    Buduje few-shot prompt z opisem zadania, przykładami i nowym zapytaniem.
    
    Args:
        task_description: Opis zadania dla AI
        examples: Lista krotek (input, output)
        user_input: Nowe zapytanie do klasyfikacji
        example_separator: Separator między przykładami
        
    Returns:
        Sformatowany few-shot prompt
    """
    prompt = task_description + "\n\n"
    
    if examples:
        prompt += "PRZYKŁADY:\n"
        for i, (example_input, example_output) in enumerate(examples, 1):
            prompt += f"Przykład {i}:\n"
            prompt += f"Input: {example_input}\n"
            prompt += f"Output: {example_output}\n"
            if i < len(examples):
                prompt += example_separator
        prompt += "\n---\n\n"
    
    prompt += f"Twoje zapytanie:\n{user_input}"
    
    return prompt


def ask_openrouter_few_shot(
    task_description: str,
    examples: list[FewShotExample],
    user_input: str,
    model: str = "openai/gpt-3.5-turbo",
    conversation_history: Union[list[dict[str, str]], None] = None
) -> str:
    """
    Wysyła few-shot prompt do OpenRouter API.
    
    Args:
        task_description: Opis zadania
        examples: Lista krotek (input, output) - przykłady
        user_input: Nowe zapytanie
        model: Model do użycia
        conversation_history: Historia konwersacji (opcjonalnie)
        
    Returns:
        Odpowiedź od AI
        
    Example:
        examples = [
            ("Aplikacja się zawiesza", "bug"),
            ("Dodaj eksport PDF", "feature_request"),
            ("Jak logować się?", "question"),
        ]
        result = ask_openrouter_few_shot(
            "Klasyfikuj wiadomości na: bug, feature_request, question",
            examples,
            "Przycisk nie działa na mobile"
        )
    """
    if conversation_history is None:
        conversation_history = []
    
    prompt = build_few_shot_prompt(task_description, examples, user_input)
    return ask_openrouter(prompt, conversation_history, model)


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
