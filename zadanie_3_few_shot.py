"""
Zadanie 3 — Few-shot prompting
Klasyfikacja wiadomości użytkownika na kategorie: bug, feature_request, question
"""

from openrouter import ask_openrouter_few_shot


# Few-shot przykłady dla klasyfikacji
CLASSIFICATION_EXAMPLES = [
    ("Aplikacja się zawiesza po kliknięciu przycisku Zapisz", "bug"),
    ("Czy możlibyście dodać możliwość eksportu do PDF?", "feature_request"),
    ("Jak zmienić język interfejsu?", "question"),
]

TASK_DESCRIPTION = """Klasyfikuj wiadomość użytkownika na jedną z trzech kategorii:
- bug: problem techniczny, błąd w aplikacji
- feature_request: prośba o nową funkcjonalność
- question: pytanie dotyczące użytkowania

Odpowiedź podaj w formacie: Category: [kategoria]
Confidence: [high/medium/low]
Explanation: [krótkie wyjaśnienie]"""


def classify_message(user_message: str) -> dict:
    """
    Klasyfikuje wiadomość użytkownika na jedną z trzech kategorii
    używając few-shot promptingu.
    
    Args:
        user_message: wiadomość do klasyfikacji
        
    Returns:
        dict z polami: message, category, confidence, explanation
    """
    response = ask_openrouter_few_shot(
        task_description=TASK_DESCRIPTION,
        examples=CLASSIFICATION_EXAMPLES,
        user_input=user_message
    )
    
    # Parsowanie odpowiedzi
    result = {
        "original_message": user_message,
        "response": response,
        "category": None,
        "confidence": None,
        "explanation": None
    }
    
    # Prosta analiza odpowiedzi
    lines = response.split('\n')
    for line in lines:
        if 'Category:' in line:
            category_str = line.split('Category:')[1].strip().lower()
            # Wyciągnij kategorię
            if 'bug' in category_str:
                result['category'] = 'bug'
            elif 'feature_request' in category_str or 'feature request' in category_str:
                result['category'] = 'feature_request'
            elif 'question' in category_str:
                result['category'] = 'question'
        elif 'Confidence:' in line:
            confidence_str = line.split('Confidence:')[1].strip().lower()
            if 'high' in confidence_str:
                result['confidence'] = 'high'
            elif 'medium' in confidence_str:
                result['confidence'] = 'medium'
            elif 'low' in confidence_str:
                result['confidence'] = 'low'
        elif 'Explanation:' in line or 'Uzasadnienie:' in line:
            result['explanation'] = line.split(':')[1].strip()
    
    return result



def test_few_shot_classification():
    """Testuje few-shot prompting na 5 przykładowych wiadomościach"""
    
    test_messages = [
        "Przycisk logowania nie działa na urządzeniach mobilnych",
        "Chciałbym mieć możliwość wysyłania załączników",
        "Na jakie typy plików są ograniczenia?",
        "Program zawala się gdy usunę konwersację",
        "Czy planujecie dodać opcję dark mode?"
    ]
    
    print("=" * 80)
    print("ZADANIE 3 — Few-shot Prompting — Klasyfikacja Wiadomości")
    print("=" * 80)
    print()
    
    results = []
    
    for idx, message in enumerate(test_messages, 1):
        print(f"TEST {idx}/5")
        print(f"Wiadomość: {message}")
        print("-" * 80)
        
        result = classify_message(message)
        results.append(result)
        
        print(f"✓ Kategoria: {result['category'].upper() if result['category'] else 'NIEZNANA'}")
        print(f"✓ Pewność: {result['confidence'].upper() if result['confidence'] else 'NIEZNANA'}")
        if result['explanation']:
            print(f"✓ Wyjaśnienie: {result['explanation']}")
        print()
        print("Pełna odpowiedź z API:")
        print(result['response'])
        print("\n" + "=" * 80 + "\n")
    
    # Podsumowanie
    print("PODSUMOWANIE WYNIKÓW:")
    print("-" * 80)
    
    categories_count = {"bug": 0, "feature_request": 0, "question": 0}
    
    for idx, result in enumerate(results, 1):
        category = result['category'] or "NIEZNANA"
        categories_count[category] = categories_count.get(category, 0) + 1
        print(f"{idx}. [{category.upper()}] {result['original_message']}")
    
    print("-" * 80)
    print("Statystyka kategorii:")
    for category, count in categories_count.items():
        if category in ["bug", "feature_request", "question"]:
            print(f"  • {category}: {count}")
    
    return results


if __name__ == "__main__":
    test_few_shot_classification()
