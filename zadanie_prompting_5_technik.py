
# Nowy model: lista zadań
class TaskList(BaseModel):
    tasks: List[ProgrammingTask]

import json
# =====================
# Zadanie 5 — Generowanie zadań przez AI + walidacja
# =====================

# Nowa funkcja: generuje listę 3 zadań
def get_ai_programming_tasks() -> str:
    """
    Symuluje odpowiedź AI na prompt o listę zadań programistycznych.
    Zwraca JSON: {"tasks": [ ... ]}
    """
    import random
    valid_task = {
        "task_name": "API do notatek",
        "difficulty": random.choice(["easy", "medium", "hard"]),
        "estimated_minutes": random.choice([15, 30, 45]),
        "steps": [
            {"step": 1, "description": "Stwórz endpoint POST /notes"},
            {"step": 2, "description": "Dodaj walidację danych"}
        ]
    }
    # Tworzymy 3 zadania, jedno może być błędne
    tasks = [valid_task.copy() for _ in range(3)]
    # Wariant z jednym błędnym zadaniem
    if random.random() < 0.5:
        tasks[1]["difficulty"] = "trivial"  # niepoprawna trudność
        tasks[2]["estimated_minutes"] = 0    # niepoprawny czas
    return json.dumps({"tasks": tasks}, ensure_ascii=False)

# Nowa funkcja do zadania dodatkowego
def zadanie5_lista():
    print("\n--- Zadanie dodatkowe: Lista zadań AI + walidacja ---")
    prompt = "Wygeneruj 3 zadania programistyczne dla praktykanta backendu. Odpowiedź w formacie JSON: {tasks: [ ... ]}"
    print("Prompt:", prompt)
    ai_response = get_ai_programming_tasks()
    print("Odpowiedź AI:", ai_response)
    try:
        data = json.loads(ai_response)
        task_list = TaskList(**data)
        # Sprawdzenie liczby zadań
        if len(task_list.tasks) != 3:
            print(f"Błąd: lista zadań zawiera {len(task_list.tasks)} elementów zamiast 3!")
        else:
            print("Liczba zadań OK: 3")
        # Sprawdzenie walidacji każdego zadania
        for i, task in enumerate(task_list.tasks, 1):
            print(f"Zadanie {i}: {task}")
        print("Wszystkie zadania przeszły walidację!")
    except ValidationError as e:
        print("Błąd walidacji listy zadań:", e)
        print("Zapisuję odpowiedź do invalid_response_list.json...")
        with open("invalid_response_list.json", "w", encoding="utf-8") as f:
            f.write(ai_response)

if __name__ == "__main__":
    # ...existing code...
    zadanie5_lista()
# =====================
# Zadanie 4 — Bardziej złożony model
# =====================

from typing import List
from pydantic import BaseModel, ValidationError, field_validator

class TaskStep(BaseModel):
    step: int
    description: str


class ProgrammingTask(BaseModel):
    task_name: str
    difficulty: str
    estimated_minutes: int
    steps: List[TaskStep]

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v):
        allowed = {"easy", "medium", "hard"}
        if v not in allowed:
            raise ValueError(f"difficulty must be one of {allowed}")
        return v

    @field_validator('estimated_minutes')
    @classmethod
    def validate_minutes(cls, v):
        if v <= 0:
            raise ValueError("estimated_minutes must be > 0")
        return v



# Przykład użycia i test walidacji
if __name__ == "__main__":
    # ...existing code...
    print("\n--- Zadanie 4: Walidacja ProgrammingTask ---")
    valid_data = {
        "task_name": "FizzBuzz",
        "difficulty": "easy",
        "estimated_minutes": 10,
        "steps": [
            {"step": 1, "description": "Napisz pętlę od 1 do 100"},
            {"step": 2, "description": "Dla wielokrotności 3 wypisz 'Fizz'"},
            {"step": 3, "description": "Dla wielokrotności 5 wypisz 'Buzz'"},
        ]
    }
    try:
        task = ProgrammingTask(**valid_data)
        print("Poprawna walidacja:", task)
    except ValidationError as e:
        print("Błąd walidacji:", e)

    invalid_data = {
        "task_name": "FizzBuzz",
        "difficulty": "trivial",
        "estimated_minutes": -5,
        "steps": [
            {"step": 1, "description": "Napisz pętlę od 1 do 100"}
        ]
    }
    try:
        task = ProgrammingTask(**invalid_data)
        print("Poprawna walidacja:", task)
    except ValidationError as e:
        print("Błąd walidacji (błędne dane):", e)
# Definicje funkcji i klas powyżej...

## Usunięto powielony blok wywołań niezdefiniowanych funkcji zadanie2 i zadanie3
import json

import json
import random
from pydantic import BaseModel, ValidationError

class ArticleSummary(BaseModel):
    title: str
    summary: str
    tags: list[str]

def get_ai_summary(text: str) -> str:
    """
    Funkcja symulująca odpowiedź AI na podsumowanie tekstu.
    W prawdziwej aplikacji tu byłoby wywołanie API.
    """
    responses = [
        '{"title": "Nowości AI", "summary": "Podsumowanie o AI.", "tags": ["AI", "podsumowanie"]}',
        '{"title": "Nowości AI", "summary": "Podsumowanie o AI.", "tags": "AI"}',
        '{"summary": "Podsumowanie o AI.", "tags": ["AI", "podsumowanie"]}'
    ]
    return random.choice(responses)

def popraw_json_ai(zly_json: str, schema: str) -> str:
    """
    Symuluje poprawę niepoprawnego JSON przez AI.
    W prawdziwej aplikacji tu byłoby wywołanie API z promptem naprawiającym.
    """
    return '{"title": "Naprawiony tytuł", "summary": "Naprawione podsumowanie.", "tags": ["AI", "naprawa"]}'

def zadanie2(text: str):
    print("\n--- Zadanie 2: AI + walidacja ---")
    prompt = (
        "Podsumuj poniższy tekst i zwróć wynik w JSON.\n"
        "Format:\n"
        '{"title": "...", "summary": "...", "tags": ["...", "..."]}'
    )
    print("Prompt:", prompt)
    print("Tekst:", text)
    ai_response = get_ai_summary(text)
    print("Odpowiedź AI:", ai_response)
    try:
        data = json.loads(ai_response)
        article = ArticleSummary(**data)
        print("Poprawna walidacja:", article)
    except ValidationError as e:
        print("Błąd walidacji:", e)
        print("Odpowiedź modelu:", ai_response)

def zadanie3(text: str):
    print("\n--- Zadanie 3: AI + walidacja + automatyczna poprawa ---")
    prompt = (
        "Podsumuj poniższy tekst i zwróć wynik w JSON.\n"
        "Format:\n"
        '{"title": "...", "summary": "...", "tags": ["...", "..."]}'
    )
    print("Prompt:", prompt)
    print("Tekst:", text)
    ai_response = get_ai_summary(text)
    print("Odpowiedź AI:", ai_response)
    try:
        data = json.loads(ai_response)
        article = ArticleSummary(**data)
        print("Poprawna walidacja:", article)
    except ValidationError as e:
        print("Błąd walidacji:", e)
        print("Odpowiedź modelu:", ai_response)
        print("Próba automatycznej poprawy JSON przez AI...")
        schema = '{"title": "str", "summary": "str", "tags": ["str"]}'
        poprawiony_json = popraw_json_ai(ai_response, schema)
        print("Poprawiony JSON od AI:", poprawiony_json)
        try:
            data2 = json.loads(poprawiony_json)
            article2 = ArticleSummary(**data2)
            print("Poprawna walidacja po poprawce:", article2)
        except ValidationError as e2:
            print("Nadal błąd walidacji po poprawce:", e2)


# Blok uruchomieniowy
if __name__ == "__main__":
    zadanie2("Sztuczna inteligencja rozwija się bardzo szybko i zmienia świat.")
    zadanie3("Sztuczna inteligencja rozwija się bardzo szybko i zmienia świat.")

def popraw_json_ai(zly_json: str, schema: str) -> str:
    """
    Symuluje poprawę niepoprawnego JSON przez AI.
    W prawdziwej aplikacji tu byłoby wywołanie API z promptem naprawiającym.
    """
    # Zwraca poprawny JSON zgodny ze schematem
    return '{"title": "Naprawiony tytuł", "summary": "Naprawione podsumowanie.", "tags": ["AI", "naprawa"]}'

def zadanie3(text: str):
    print("\n--- Zadanie 3: AI + walidacja + automatyczna poprawa ---")
    prompt = (
        "Podsumuj poniższy tekst i zwróć wynik w JSON.\n"
        "Format:\n"
        '{"title": "...", "summary": "...", "tags": ["...", "..."]}'
    )
    print("Prompt:", prompt)
    print("Tekst:", text)
    ai_response = get_ai_summary(text)
    print("Odpowiedź AI:", ai_response)
    try:
        data = json.loads(ai_response)
        article = ArticleSummary(**data)
        print("Poprawna walidacja:", article)
    except ValidationError as e:
        print("Błąd walidacji:", e)
        print("Odpowiedź modelu:", ai_response)
        # Automatyczna poprawa przez AI
        print("Próba automatycznej poprawy JSON przez AI...")
        schema = '{"title": "str", "summary": "str", "tags": ["str"]}'
        poprawiony_json = popraw_json_ai(ai_response, schema)
        print("Poprawiony JSON od AI:", poprawiony_json)
        try:
            data2 = json.loads(poprawiony_json)
            article2 = ArticleSummary(**data2)
            print("Poprawna walidacja po poprawce:", article2)
        except ValidationError as e2:
            print("Nadal błąd walidacji po poprawce:", e2)

"""
5 Różnych Promptów - Techniki i Strategie Promptingu
Demonstracja różnych podejść do interakcji z AI
"""

from openrouter import ask_openrouter


# PROMPT 1: ZERO-SHOT (bez przykładów)
ZERO_SHOT_PROMPT = """Klasyfikuj poniższą wiadomość użytkownika na jedną z trzech kategorii:
- bug (problem techniczny)
- feature_request (prośba o nową funkcję)
- question (pytanie)

Wiadomość: {message}

Odpowiedź podaj w jednej linii w formacie: Category: [nazwa]"""


# PROMPT 2: FEW-SHOT (z przykładami)
FEW_SHOT_PROMPT = """Klasyfikuj wiadomości na jedną z trzech kategorii: bug, feature_request, question
class ArticleSummary(BaseModel):
    title: str
    summary: str
    tags: list[str]

PRZYKŁADY:
- "Aplikacja się zawiesza" → bug
- "Dodajcie eksport PDF" → feature_request
- "Jak logować się po zmianie hasła?" → question

Teraz klasyfikuj:
Wiadomość: {message}
Category: """


# PROMPT 3: CHAIN-OF-THOUGHT (rozumowanie krok po kroku)
CHAIN_OF_THOUGHT_PROMPT = """Przeanalizuj wiadomość i klasyfikuj na: bug, feature_request, question

Kroki analizy:
1. Identyfikuj cel komunikacji (problem, prośba, pytanie)
2. Określ typ zgłoszenia
3. Podaj kategorię

Wiadomość: {message}

Analiza:
- Cel komunikacji:
- Typ zgłoszenia:
- Kategoria: """


# PROMPT 4: ROLE-BASED (z przypisaną rolą)
ROLE_BASED_PROMPT = """Jesteś doświadczonym customer support manager. Twoja rola to klasyfikować wiadomości użytkowników.

Przeanalizuj tę wiadomość i określ jej typ:
"{message}"

Jako customer support manager, powiedz:
1. Jaki jest problem/pytanie użytkownika?
2. Do której kategorii to należy? (bug/feature_request/question)
3. Jaki jest priorytet? (high/medium/low)
4. Jaka powinna być odpowiedź zespołu?"""


# PROMPT 5: STRUCTURED OUTPUT (ustrukturyzowana odpowiedź)
STRUCTURED_OUTPUT_PROMPT = """Przeanalizuj i klasyfikuj wiadomość. Odpowiedź podaj w następującym formacie JSON:

{{
    "message": "oryginalna wiadomość",
    "category": "bug|feature_request|question",
    "confidence": "high|medium|low",
    "keywords": ["lista", "kluczowych", "słów"],
    "sentiment": "positive|neutral|negative",

    "suggested_response_type": "technical_fix|roadmap_discussion|documentation|other"
}
Wiadomość do klasyfikacji: {message}

JSON:"""


def test_prompt(prompt_name: str, prompt_template: str, test_message: str) -> dict:
    """Testuje prompt i zwraca rezultat"""
    print(f"\n{'='*80}")
    print(f"PROMPT: {prompt_name}")
    print(f"{'='*80}")
    print(f"Wiadomość: {test_message}\n")
    print("Szablon promptu:")
    print("-" * 80)
    print(prompt_template.replace("{message}", f"[{test_message}]"))
    print("-" * 80)
    
    prompt = prompt_template.format(message=test_message)
    conversation_history = []
    
    print("\n[TRYB DEMO] Wywołanie AI zostało wyłączone. Zwracana jest przykładowa odpowiedź.")
    # Przykładowa odpowiedź do testów walidacji
    response = '{"title": "Przykładowy tytuł", "summary": "Przykładowe podsumowanie.", "tags": ["AI", "test"]}'
    print("\nOdpowiedź AI:")
    print(response)
    return {
        "prompt_name": prompt_name,
        "message": test_message
    }

def main():
    """Główna funkcja - testuje 5 promptów"""
    
    prompts = [
        ("1. ZERO-SHOT", ZERO_SHOT_PROMPT),
        ("2. FEW-SHOT", FEW_SHOT_PROMPT),
        ("3. CHAIN-OF-THOUGHT", CHAIN_OF_THOUGHT_PROMPT),
        ("4. ROLE-BASED", ROLE_BASED_PROMPT),
        ("5. STRUCTURED OUTPUT", STRUCTURED_OUTPUT_PROMPT),
    ]
    
    # Wiadomość testowa
    test_message = "Aplikacja się zawiesza gdy wysyłam dużą wiadomość"
    
    all_results = []
    
    for prompt_name, prompt_template in prompts:
        result = test_prompt(prompt_name, prompt_template, test_message)
        all_results.append(result)
    
    # Podsumowanie
    print(f"\n\n{'='*80}")
    print("PODSUMOWANIE - 5 PROMPTÓW")
    print(f"{'='*80}\n")
    
    for idx, result in enumerate(all_results, 1):
        status = "✓ OK" if result['success'] else "✗ BŁĄD"
        print(f"{idx}. {result['prompt_name']}: {status}")
    
    # Szczegółowe porównanie podejść
    print(f"\n{'='*80}")
    print("PORÓWNANIE TECHNIK PROMPTINGU")
    print(f"{'='*80}\n")
    
    comparison = {
        "Zero-shot": {
            "opis": "Bez przykładów - model sam decyduje",
            "zaleta": "Szybkie, minimalna ilość tokenów",
            "wada": "Mniej spójne wyniki, może źle zinterpretować"
        },
        "Few-shot": {
            "opis": "Z przykładami - nauczanie przez pokazanie",
            "zaleta": "Bardzo efektywne, spójne wyniki",
            "wada": "Więcej tokenów, muszą być dobre przykłady"
        },
        "Chain-of-thought": {
            "opis": "Rozumowanie krok po kroku",
            "zaleta": "Transparentny proces, łatwo debugować",
            "wada": "Dłuższe odpowiedzi, większe koszty"
        },
        "Role-based": {
            "opis": "Przypisanie roli/kontekstu",
            "zaleta": "Personalizacja, lepszy kontekst",
            "wada": "Może być zbyt verbose, zależy od roli"
        },
        "Structured output": {
            "opis": "Żądanie konkretnego formatu",
            "zaleta": "Łatwy do parsowania, automatyzacja",
            "wada": "Model musi znać format, może go zignorować"
        }
    }
    
    for idx, (technique, details) in enumerate(comparison.items(), 1):
        print(f"{idx}. {technique}")
        print(f"   📝 {details['opis']}")
        print(f"   ✓  Zaleta: {details['zaleta']}")
        print(f"   ✗  Wada: {details['wada']}\n")
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
