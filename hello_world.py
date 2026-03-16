import os
import sqlite3
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv


load_dotenv()


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def run_postgres_flow():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    conn.autocommit = True
    cur = conn.cursor()

    print("Połączono z bazą PostgreSQL.")
    cur.execute("SELECT current_database(), current_schema();")
    db_name, schema_name = cur.fetchone()
    print(f"Aktywna baza: {db_name}, aktywny schemat: {schema_name}")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS public.messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    print("Tabela 'messages' gotowa.")

    wiadomosc = "Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊"
    cur.execute("INSERT INTO public.messages (content) VALUES (%s) RETURNING id;", (wiadomosc,))
    nowy_id = cur.fetchone()[0]
    print(f"Wstawiono wiadomość o ID: {nowy_id}")

    cur.execute("SELECT content, created_at FROM public.messages ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    if row:
        print(f"Odczytano: '{row[0]}' (z {row[1]})")

    cur.close()
    conn.close()
    print("Połączenie zamknięte.")


def run_sqlite_fallback_flow():
    conn = sqlite3.connect("local_fallback.db")
    cur = conn.cursor()

    print("Uruchomiono tryb awaryjny SQLite (plik local_fallback.db).")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    print("Tabela 'messages' gotowa.")

    wiadomosc = "Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊"
    cur.execute("INSERT INTO messages (content) VALUES (?);", (wiadomosc,))
    nowy_id = cur.lastrowid
    conn.commit()
    print(f"Wstawiono wiadomość o ID: {nowy_id}")

    cur.execute("SELECT content, created_at FROM messages ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    if row:
        print(f"Odczytano: '{row[0]}' (z {row[1]})")

    cur.close()
    conn.close()
    print("Połączenie zamknięte.")


try:
    run_postgres_flow()
except OperationalError as e:
    error_text = str(e)
    print(f"Błąd połączenia z bazą PostgreSQL: {error_text}")
    if "Connection refused" in error_text or "could not connect to server" in error_text:
        print(
            "PostgreSQL nie działa. Uruchamiam tryb awaryjny SQLite. "
            "Aby wrócić do PostgreSQL, uruchom bazę i ponów próbę."
        )
        run_sqlite_fallback_flow()
    else:
        raise
except Exception as e:
    print(f"Błąd: {e}")