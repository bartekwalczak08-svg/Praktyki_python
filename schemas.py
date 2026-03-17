from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List


# --- Enum dla ról w konwersacji ---

class MessageRole(str, Enum):
    """Enumeration dla ról w konwersacji"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


# --- Schematy dla Messages ---

class MessageBase(BaseModel):
    """Bazowy schemat wiadomości"""
    content: str = Field(..., min_length=1, max_length=10000, description="Zawartość wiadomości")


class MessageCreate(MessageBase):
    """Schemat do tworzenia nowej wiadomości"""
    pass


class MessageResponse(MessageBase):
    """Schemat odpowiedzi z bazą danych"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # kompatybilność z SQLAlchemy
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊",
                "created_at": "2026-03-17T09:16:11.150471"
            }
        }


# --- Schematy dla Conversations ---

class ConversationBase(BaseModel):
    """Bazowy schemat konwersacji"""
    session_id: str = Field(..., min_length=1, max_length=50, description="ID sesji")
    role: MessageRole = Field(..., description="Rola: system, user lub assistant")
    content: str = Field(..., min_length=1, max_length=10000, description="Treść wiadomości")


class ConversationCreate(ConversationBase):
    """Schemat do tworzenia nowej konwersacji"""
    pass


class ConversationResponse(ConversationBase):
    """Schemat odpowiedzi konwersacji z bazy danych"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "session_id": "sess_123abc",
                "role": "user",
                "content": "Jak się masz?",
                "created_at": "2026-03-17T09:16:11.150471"
            }
        }


# --- Schema dla historii konwersacji (do API) ---

class ChatMessage(BaseModel):
    """Schemat pojedynczej wiadomości w czacie"""
    role: MessageRole
    content: str


class ChatHistory(BaseModel):
    """Schemat historii konwersacji"""
    messages: List[ChatMessage]
