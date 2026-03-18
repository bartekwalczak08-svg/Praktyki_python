
import os
import requests
from dotenv import load_dotenv

load_dotenv()

## Zadanie 1
##Przeanalizuj poniższe payload'e. Które są poprawne, a które błędne?

# ❓ PAYLOAD A - poprawny
payload_a = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Cześć, jak się masz?"},
        {"role": "user", "content": "Odpowiedz mi na pytanie"}
    ],
    "temperature": 0.7
}

# ❓ PAYLOAD B - błędny
payload_b = {
    "model": "",
    "messages": [
        {"role": "user", "content": "Jesteś ekspertem w Pythonie"},
        {"role": "system", "content": "Pomóż mi debugować kod"}
    ],
    "temperature": 0.7
}

# ❓ PAYLOAD C - poprawny
payload_c = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Jesteś poliglotą. Mówisz 50 językami."},
        {"role": "user", "content": "Przetłumacz 'Hello' na polski"}
    ],
    "temperature": 0.5
}

# ❓ PAYLOAD D - błędny
payload_d = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Rozwiąż to równanie: 2x + 5 = 15"},
        {"role": "user", "content": "Jestem uczniem"}
    ],
    "temperature": 0.2
}



## Zadanie 2
##Stwórz 5 payload'ów dla różnych scenariuszy. Każdy powinien mieć dobrze sformułowany system i user:

# 1️⃣ KALKULATOR NAUKOWY
payload_1 = {
    "model": "",
    "messages": [
        {
            "role": "system",
            "content": "Jesteś zaawansowanym kalkulatorem naukowym. Potrafisz rozwiązywać skomplikowane równania, wykonywać obliczenia matematyczne i udzielać precyzyjnych odpowiedzi."
        },
        {
            "role": "user",
            "content": "Oblicz sin(45°) + cos(30°) i podaj wynik z dokładnością do 4 miejsc po przecinku."
        }
    ],
    "temperature": 0.1,  # ❄️ Czemu niska?
    "max_tokens": 200
}


# 2️⃣ NAUCZYCIEL ANGIELSKIEGO
payload_2 = {
    "model": "",
    "messages": [
        {
            "role": "system",
            "content": (
                "Jestes nauczycielem jezyka angielskiego dla poziomu B1. "
                "Odpowiadasz jasno i krotko. Najpierw podajesz poprawiona wersje tekstu, "
                "nastepnie wyjasniasz najwazniejsze bledy po polsku, a na koncu dajesz 2 "
                "krotkie cwiczenia utrwalajace."
            )
        },
        {
            "role": "user",
            "content": (
                "Sprawdz i popraw moje zdanie: 'I have 25 years old and I working in IT since 3 years.' "
                "Wyjasnij bledy po polsku i daj 2 krotkie cwiczenia na Present Perfect vs Present Simple."
            )
        }
    ],
    "temperature": 0.6,
    "max_tokens": 300
}

# 3️⃣ COPYWRITER MARKETINGOWY
payload_3 = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Jesteś kreatywnym copywriterem marketingowym. Tworzysz chwytliwe slogany i teksty reklamowe."},
        {"role": "user", "content": "Stwórz slogan reklamowy dla nowej kawiarni w centrum miasta."}
    ],
    "temperature": 1.2,
    "max_tokens": 250
}

# 4️⃣ PSYCHOLOG
payload_4 = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Jesteś doświadczonym psychologiem. Udzielasz wsparcia emocjonalnego i porad w trudnych sytuacjach."},
        {"role": "user", "content": "Czuję się zestresowany i przytłoczony obowiązkami. Co mogę zrobić, aby się uspokoić?"}
    ],
    "temperature": 0.8,
    "max_tokens": 500
}

# 5️⃣ DEBUGGER KODU
payload_5 = {
    "model": "",
    "messages": [
        {"role": "system", "content": "Jesteś Debuggerem kodu. Pomagasz znaleźć błędy w kodzie i sugerujesz rozwiązania problemów."},
        {"role": "user", "content": "Pomóż mi naprawić kod w Pythonie, który zwraca błąd 'IndexError: list index out of range'."}
    ],
    "temperature": 0.2,
    "max_tokens": 400
}

## Zadanie 3 - dodatkowe
## Napisz/przerób istniejący kod, który wysyła to samo pytanie 3 razy z różnymi wartościami temperature:

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

prompt = "Wymyśl kreatywny slogan dla kawiarni"
temperatures = [0.0, 0.7, 2.0]
odpowiedzi = []


def send_chat_request(messages, temperature, max_tokens=100):
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def normalize_high_temperature_output(text):
    return send_chat_request(
        [
            {
                "role": "system",
                "content": (
                    "Uporzadkuj odpowiedz do jednej, albo dwóch krotkiej, poprawnej i naturalnej linijki po polsku. "
                    "Jesteś kreatywnym copywriterem. Stworz chwytliwy slogan dla kawiarni. "
                    "Jesli tekst jest chaotyczny lub bez sensu, stworz od nowa jeden sensowny slogan dla kawiarni."
                )
            },
            {
                "role": "user",
                "content": f"Uporzadkuj ten tekst: {text}"
            }
        ],
        temperature=0.2,
        max_tokens=60,
    )

for temp in temperatures:
    tekst = send_chat_request(
        [
            {
                "role": "system",
                "content": "Jesteś ekspertem w sprawach polityki. Masz wybrać najlepszą partię spośród Pis,Po,Konfederacji i lewicy."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temp,
    )

    if temp >= 2.0:
        tekst = normalize_high_temperature_output(tekst)

    odpowiedzi.append(tekst)

    print(f"\n--- Temperature: {temp} ---")
    print(tekst)

print("\n===== PORÓWNANIE =====")
for temp, odp in zip(temperatures, odpowiedzi):
    print(f"[temp={temp}] długość: {len(odp)} znaków | unikalnych słów: {len(set(odp.lower().split()))}")
    print(f"  Odpowiedź: {odp[:80]}{'...' if len(odp) > 80 else ''}")