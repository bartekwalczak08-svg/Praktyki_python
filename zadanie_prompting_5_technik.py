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
}}

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
    
    try:
        response = ask_openrouter(prompt, conversation_history, model="openai/gpt-3.5-turbo")
        print("\nOdpowiedź AI:")
        print(response)
        
        return {
            "prompt_name": prompt_name,
            "message": test_message,
            "response": response,
            "success": True
        }
    except Exception as e:
        print(f"\n❌ Błąd: {str(e)}")
        return {
            "prompt_name": prompt_name,
            "message": test_message,
            "error": str(e),
            "success": False
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
