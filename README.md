# Python Docker DB - Praktyki Programistyczne

Projekt zawiera przykład pracy z bazą PostgreSQL, migracjami Alembic, schematami Pydantic i OpenRouter API.

## Struktura Projektu

```
.
├── alembic/                    # Migracje bazy danych
│   ├── versions/
│   │   ├── 75266909ac49_create_messages_table.py
│   │   └── e512bf7a0a13_create_conversations_table.py
│   ├── env.py                  # Konfiguracja Alembica
│   └── script.py.mako
├── alembic.ini                 # Config Alembica
├── models.py                   # Modele SQLAlchemy
├── schemas.py                  # Schematy Pydantic
├── main.py                     # Główna aplikacja
├── openrouter.py               # Klient OpenRouter API
├── docker-compose.yml          # PostgreSQL container
├── requirements.txt            # Zależności Python
└── .env.example                # Szablon zmiennych środowiskowych
```

## Instalacja

### 1. Klonowanie projektu
```bash
git clone https://github.com/bartekwalczak08-svg/Praktyki_python.git
cd python-docker-db
```

### 2. Instalacja zależności
```bash
# Windows (PowerShell)
.venv\Scripts\pip install -r requirements.txt

# Linux/macOS
pip install -r requirements.txt
```

### 3. Konfiguracja zmiennych środowiskowych
```bash
cp .env.example .env
# Edytuj .env i wpisz swoje dane bazy i klucz OpenRouter API
```

## Uruchamianie

### 1. Start PostgreSQL w Docker (WSL2)
```bash
# Z terminala WSL
docker compose up -d
```

### 2. Sprawdzenie statusu bazy
```bash
docker compose ps
docker compose logs db
```

### 3. Uruchomienie aplikacji
```bash
# Z PowerShell (Windows)
.venv\Scripts\python main.py

# Linux/macOS
python main.py
```

## Migracje Alembic

### Sprawdzenie bieżącej wersji
```bash
.venv\Scripts\alembic current
```

### Aplikowanie nowych migracji
```bash
.venv\Scripts\alembic upgrade head
```

### Cofnięcie do poprzedniej wersji
```bash
.venv\Scripts\alembic downgrade -1
```

### Generowanie nowej migracji
1. Edytuj [models.py](models.py)
2. Uruchom:
```bash
.venv\Scripts\alembic revision --autogenerate -m "opis zmian"
.venv\Scripts\alembic upgrade head
```

## Baza Danych

### Tabele

#### `messages`
- `id` (SERIAL PRIMARY KEY)
- `content` (TEXT NOT NULL)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

#### `conversations`
- `id` (SERIAL PRIMARY KEY)
- `session_id` (VARCHAR(50) NOT NULL) — ID sesji
- `role` (VARCHAR(20) NOT NULL) — 'system', 'user', lub 'assistant'
- `content` (TEXT NOT NULL)
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

### Dostęp do bazy z CLI
```bash
docker exec -it moja-baza psql -U testuser -d testdb

# Wewnątrz psql:
\dt                  # Lista tabel
SELECT * FROM messages;
SELECT * FROM conversations WHERE session_id = 'sess_123';
\q                   # Wyjście
```

## API Schematy (Pydantic)

### Messages
- `MessageCreate`: { content }
- `MessageResponse`: { id, content, created_at }

### Conversations
- `ConversationCreate`: { session_id, role, content }
- `ConversationResponse`: { id, session_id, role, content, created_at }

### Chat History
- `ChatMessage`: { role, content }
- `ChatHistory`: { messages: List[ChatMessage] }

### Role Enum
- `SYSTEM` = "system"
- `USER` = "user"
- `ASSISTANT` = "assistant"

## Requirements

- Python 3.14+
- PostgreSQL 16
- Docker / Docker Desktop z WSL2 backend

## Zmienne Środowiskowe (.env)

```env
# PostgreSQL
DB_HOST=localhost
DB_PORT=5433
DB_NAME=testdb
DB_USER=testuser
DB_PASSWORD=testpass
DATABASE_URL=postgresql+psycopg2://testuser:testpass@localhost:5433/testdb

# OpenRouter API
OPENROUTER_API_KEY=sk-or-...
```

## Troubleshooting

### Błąd: `docker is not recognized`
- Zainstaluj Docker Desktop
- Włącz WSL2 backend w ustawieniach Docker Desktop

### Błąd: `relation "messages" already exists`
- Baza już zawiera tabelę; oznacz migrację jako wykonaną:
```bash
.venv\Scripts\alembic stamp 75266909ac49
```

### Błąd: `ModuleNotFoundError: No module named 'pydantic'`
```bash
.venv\Scripts\pip install -r requirements.txt --force-reinstall
```

## Commit History

```
881c913 refactor: update schemas with base classes and chat history support
f4be40d feat: add schemas.py with Pydantic models
e780906 feat: add pydantic==2.7.1 to requirements.txt
06bb140 feat: add conversations table and second migration
a57efa1 feat: add SQLAlchemy model for Alembic autogenerate
44de7fc feat: configure Alembic to read DATABASE_URL from .env
44c506a feat: add Alembic migrations setup
ccfe8ca feat: add openrouter.py - klient OpenRouter API
```

## Autor

Rudy — Praktyki Programistyczne 2026

---

**Ostatnia aktualizacja:** 17.03.2026
