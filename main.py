"""
main.py - Główna aplikacja z obsługą bazy danych i OpenRouter API
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Message, Conversation
from openrouter import ask_openrouter
from schemas import (
    MessageResponse,
    ConversationResponse,
    ChatHistory,
    ChatMessage,
    MessageRole,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def init_db():
    """Zainicjalizuj bazę danych (tworzy tabele jeśli nie istnieją)"""
    Base.metadata.create_all(bind=engine)
    print("✓ Baza danych zainicjalizowana")


def add_message(content: str) -> MessageResponse:
    """Dodaj nową wiadomość do tabeli messages"""
    with Session(engine) as session:
        msg = Message(content=content)
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return MessageResponse(
            id=msg.id,
            content=msg.content,
            created_at=msg.created_at,
        )


def get_messages() -> list[MessageResponse]:
    """Pobierz wszystkie wiadomości z bazy"""
    with Session(engine) as session:
        messages = session.query(Message).all()
        return [
            MessageResponse(
                id=m.id,
                content=m.content,
                created_at=m.created_at,
            )
            for m in messages
        ]


def sync_conversations_to_messages() -> int:
    """Przepisz brakujące wpisy z conversations do messages bez duplikatów"""
    with Session(engine) as session:
        existing_contents = {
            row[0] for row in session.query(Message.content).all()
        }
        conversations = session.query(Conversation).order_by(Conversation.id).all()

        synced_count = 0
        for conversation in conversations:
            message_content = (
                f"[{conversation.role.upper()}][{conversation.session_id}] "
                f"{conversation.content}"
            )
            if message_content in existing_contents:
                continue

            session.add(Message(content=message_content))
            existing_contents.add(message_content)
            synced_count += 1

        if synced_count:
            session.commit()

        return synced_count


def summarize_messages() -> MessageResponse:
    """Podsumuj wiadomości z tabeli messages i zapisz podsumowanie jako nową wiadomość"""
    sync_conversations_to_messages()
    messages = [
        message
        for message in get_messages()
        if not message.content.startswith("[PODSUMOWANIE]")
    ]

    if not messages:
        raise ValueError("Brak wiadomości w tabeli messages do podsumowania.")

    formatted_messages = "\n".join(
        f"- [{message.created_at}] {message.content}"
        for message in messages
    )
    conversation_history = [
        {
            "role": "system",
            "content": f"Wiadomości do podsumowania:\n{formatted_messages}",
        }
    ]

    summary = ask_openrouter("Podsumuj te wiadomości", conversation_history)
    return add_message(f"[PODSUMOWANIE] {summary}")


def add_conversation(
    session_id: str,
    role: MessageRole,
    content: str,
) -> ConversationResponse:
    """Dodaj nowy rekord konwersacji"""
    with Session(engine) as session:
        conv = Conversation(
            session_id=session_id,
            role=role.value,
            content=content,
        )
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return ConversationResponse(
            id=conv.id,
            session_id=conv.session_id,
            role=MessageRole(conv.role),
            content=conv.content,
            created_at=conv.created_at,
        )


def get_conversation_history(session_id: str) -> ChatHistory:
    """Pobierz historię konwersacji dla danej sesji"""
    with Session(engine) as session:
        conversations = session.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.id).all()

        messages = [
            ChatMessage(
                role=MessageRole(c.role),
                content=c.content,
            )
            for c in conversations
        ]
        return ChatHistory(messages=messages)


def list_sessions() -> list[str]:
    """Zwróć listę unikalnych session_id z tabeli conversations"""
    with Session(engine) as session:
        rows = (
            session.query(Conversation.session_id)
            .distinct()
            .order_by(Conversation.session_id)
            .all()
        )
        return [r[0] for r in rows]


def chat():
    """Interaktywna pętla czatu z pamięcią w bazie danych"""
    init_db()

    # Wybór sesji
    sessions = list_sessions()
    if sessions:
        print("\n=== Dostępne sesje ===")
        for i, sid in enumerate(sessions, 1):
            print(f"  {i}. {sid}")
        print("  0. Nowa sesja")
        choice = input("\nWybierz numer sesji (Enter = nowa): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            session_id = sessions[int(choice) - 1]
        else:
            session_id = f"sess_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    else:
        session_id = f"sess_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Wczytaj historię z bazy
    history = get_conversation_history(session_id)
    conversation_history: list[dict[str, str]] = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history.messages
    ]

    print(f"\n=== Sesja: {session_id} ===")
    if conversation_history:
        print(f"Wczytano {len(conversation_history)} wiadomości z historii:")
        for msg in history.messages:
            prefix = "Ty" if msg.role == MessageRole.USER else "AI"
            snippet = msg.content[:80] + ("..." if len(msg.content) > 80 else "")
            print(f"  [{prefix}]: {snippet}")
    else:
        print("Nowa sesja – brak historii.")

    print("\nWpisz wiadomość (lub 'exit' aby zakończyć):\n")

    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDo widzenia!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "koniec"):
            print("Do widzenia!")
            break

        # Zapisz wiadomość użytkownika do bazy
        add_conversation(session_id, MessageRole.USER, user_input)
        add_message(f"[USER][{session_id}] {user_input}")

        # Wyślij do AI (ask_openrouter dopisuje user + assistant do conversation_history)
        try:
            reply = ask_openrouter(user_input, conversation_history)
        except Exception as e:
            print(f"Błąd API: {e}")
            # Cofnij ostatnie dopisanie do historii in-memory
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()
            continue

        # Zapisz odpowiedź asystenta do bazy
        add_conversation(session_id, MessageRole.ASSISTANT, reply)
        add_message(f"[ASSISTANT][{session_id}] {reply}")

        print(f"\nAI: {reply}\n")


def run_app():
    """Proste menu startowe dla czatu i podsumowania wiadomości"""
    while True:
        print("\n=== Menu ===")
        print("1. Chat")
        print("2. Podsumuj wiadomości")
        print("3. Wyjście")

        choice = input("\nWybierz opcję [1/2/3]: ").strip()

        if choice == "1":
            chat()
            continue

        if choice == "2":
            init_db()
            try:
                summary = summarize_messages()
                print("\n=== Podsumowanie ===")
                print(summary.content)
            except Exception as e:
                print(f"Błąd podczas podsumowania: {e}")
            continue

        if choice == "3":
            print("Do widzenia!")
            break

        print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    run_app()
