"""
5 Praktycznych Przykładów Few-Shot Promptingu
Każdy przykład to inne zadanie z różnymi przykładami.
"""

from openrouter import ask_openrouter_few_shot


# ──────────────────────────────────────────────────────────────────────────────
# PRZYKŁAD 1: Analiza sentymentu recenzji
# ──────────────────────────────────────────────────────────────────────────────
def przyklad_1_sentyment():
    examples = [
        ("Produkt świetny, szybka dostawa, polecam!", "pozytywny"),
        ("Zepsuł się po tygodniu, totalna klapa.", "negatywny"),
        ("Nie jest ani dobry, ani zły. Spełnia swoje zadanie.", "neutralny"),
    ]
    return ask_openrouter_few_shot(
        task_description="Określ sentyment recenzji produktu: pozytywny, negatywny lub neutralny. Odpowiedz jednym słowem.",
        examples=examples,
        user_input="Opakowanie ładne, ale sam produkt mnie rozczarował. Chyba nie zamówię ponownie.",
    )


# ──────────────────────────────────────────────────────────────────────────────
# PRZYKŁAD 2: Ekstrakcja danych kontaktowych
# ──────────────────────────────────────────────────────────────────────────────
def przyklad_2_ekstrakcja():
    examples = [
        (
            "Zadzwoń do Jana Kowalskiego pod numer 600-123-456, email: jan@firma.pl",
            "Imię: Jan Kowalski | Tel: 600-123-456 | Email: jan@firma.pl",
        ),
        (
            "Kontakt z Anną Nowak: anna.nowak@example.com, tel. 500 999 888",
            "Imię: Anna Nowak | Tel: 500 999 888 | Email: anna.nowak@example.com",
        ),
        (
            "Marek Wiśniewski, +48 721 000 111",
            "Imię: Marek Wiśniewski | Tel: +48 721 000 111 | Email: brak",
        ),
    ]
    return ask_openrouter_few_shot(
        task_description="Wyekstrahuj dane kontaktowe z tekstu. Odpowiedź: Imię: ... | Tel: ... | Email: ...",
        examples=examples,
        user_input="Proszę kontaktować się z Karoliną Dąbrowską, e-mail: k.dabrowska@test.com, telefon 888-222-333.",
    )


# ──────────────────────────────────────────────────────────────────────────────
# PRZYKŁAD 3: Ocena jakości kodu
# ──────────────────────────────────────────────────────────────────────────────
def przyklad_3_ocena_kodu():
    examples = [
        (
            "def add(a, b): return a + b",
            "Ocena: dobry | Powód: Prosta, czytelna funkcja z sensowną nazwą.",
        ),
        (
            "x = lambda a,b,c,d,e: a*b+c/d-e**2 if a>0 else b*c-d+e",
            "Ocena: zły | Powód: Lambda zbyt skomplikowana, trudna do czytania i testowania.",
        ),
        (
            "password = 'admin123'",
            "Ocena: zły | Powód: Hasło wpisane na sztywno w kodzie (hardcoded secret).",
        ),
    ]
    return ask_openrouter_few_shot(
        task_description="Oceń jakość fragmentu kodu Pythona. Odpowiedź: Ocena: [dobry/zły] | Powód: [wyjaśnienie]",
        examples=examples,
        user_input="for i in range(len(lista)): print(lista[i])",
    )


# ──────────────────────────────────────────────────────────────────────────────
# PRZYKŁAD 4: Zmiana tonu wiadomości (formalny ↔ nieformalny)
# ──────────────────────────────────────────────────────────────────────────────
def przyklad_4_zmiana_tonu():
    examples = [
        (
            "Hej, możesz mi to wysłać jutro? Dzięki!",
            "Szanowny Panie, uprzejmie proszę o przesłanie dokumentu w dniu jutrzejszym. Z wyrazami szacunku.",
        ),
        (
            "Fajny pomysł, wrzuć to na serwer jak skończysz.",
            "Dziękuję za propozycję. Proszę o wgranie pliku na serwer po zakończeniu prac.",
        ),
        (
            "Coś mi nie działa, możesz sprawdzić?",
            "Szanowna Pani, napotykam trudności techniczne i zwracam się z prośbą o weryfikację problemu.",
        ),
    ]
    return ask_openrouter_few_shot(
        task_description="Przekształć nieformalną wiadomość na formalną wiadomość biznesową.",
        examples=examples,
        user_input="Nie ma Cię w pracy, ogarniasz tego buga czy mam komuś innemu przekazać?",
    )


# ──────────────────────────────────────────────────────────────────────────────
# PRZYKŁAD 5: Priorytetyzacja zadań
# ──────────────────────────────────────────────────────────────────────────────
def przyklad_5_priorytety():
    examples = [
        (
            "Aplikacja nie uruchamia się u żadnego klienta od 2 godzin.",
            "Priorytet: KRYTYCZNY | Czas reakcji: natychmiast | Eskalacja: tak",
        ),
        (
            "Literówka w stopce strony głównej.",
            "Priorytet: NISKI | Czas reakcji: następny sprint | Eskalacja: nie",
        ),
        (
            "Strona logowania ładuje się 8 sekund.",
            "Priorytet: WYSOKI | Czas reakcji: dziś | Eskalacja: nie",
        ),
    ]
    return ask_openrouter_few_shot(
        task_description="Oceń priorytet zgłoszenia. Odpowiedź: Priorytet: [KRYTYCZNY/WYSOKI/ŚREDNI/NISKI] | Czas reakcji: [natychmiast/dziś/ten tydzień/następny sprint] | Eskalacja: [tak/nie]",
        examples=examples,
        user_input="Raport miesięczny generuje błędne dane dla jednego z dziesięciu klientów.",
    )


# ──────────────────────────────────────────────────────────────────────────────
# URUCHOMIENIE
# ──────────────────────────────────────────────────────────────────────────────
EXAMPLES = [
    ("1. ANALIZA SENTYMENTU RECENZJI",       przyklad_1_sentyment),
    ("2. EKSTRAKCJA DANYCH KONTAKTOWYCH",    przyklad_2_ekstrakcja),
    ("3. OCENA JAKOŚCI KODU",               przyklad_3_ocena_kodu),
    ("4. ZMIANA TONU WIADOMOŚCI",            przyklad_4_zmiana_tonu),
    ("5. PRIORYTETYZACJA ZGŁOSZEŃ",          przyklad_5_priorytety),
]

if __name__ == "__main__":
    print("=" * 80)
    print("5 PRZYKŁADÓW FEW-SHOT PROMPTINGU — ask_openrouter_few_shot()")
    print("=" * 80)

    for name, func in EXAMPLES:
        print(f"\n{'─' * 80}")
        print(f"  {name}")
        print(f"{'─' * 80}")
        result = func()
        print(f"  → {result}")

    print(f"\n{'=' * 80}")
    print("Wszystkie przykłady zakończone.")
    print("=" * 80)
