"""
main.py - Główna aplikacja z obsługą bazy danych i OpenRouter API
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Base, Message, Conversation
from schemas import (
    MessageCreate,
    MessageResponse,
    ConversationCreate,
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
        ).all()

        messages = [
            ChatMessage(
                role=MessageRole(c.role),
                content=c.content,
            )
            for c in conversations
        ]
        return ChatHistory(messages=messages)


def main():
    """Przykładowe użycie aplikacji"""
    # Zainicjalizuj bazę
    init_db()

    # Dodaj przykładową wiadomość
    print("\n=== Dodawanie wiadomości ===")
    msg = add_message("Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊")
    print(f"✓ Wiadomość dodana: ID={msg.id}, created_at={msg.created_at}")

    # Pobierz wszystkie wiadomości
    print("\n=== Lista wiadomości ===")
    messages = get_messages()
    for m in messages:
        print(f"  [{m.id}] {m.content[:50]}... ({m.created_at})")

    # Dodaj konwersacje
    print("\n=== Dodawanie konwersacji ===")
    conv1 = add_conversation("sess_123", MessageRole.USER, "Cześć, jak się masz?")
    print(f"✓ Konwersacja 1: {conv1.content}")

    conv2 = add_conversation(
        "sess_123",
        MessageRole.ASSISTANT,
        "Cześć! Mam się dobrze, dziękuję za pytanie.",
    )
    print(f"✓ Konwersacja 2: {conv2.content}")

    # Pobierz historię sesji
    print("\n=== Historia sesji sess_123 ===")
    history = get_conversation_history("sess_123")
    for msg in history.messages:
        print(f"  [{msg.role}]: {msg.content}")

    print("\n✓ Aplikacja działa prawidłowo!")


if __name__ == "__main__":
    main()
