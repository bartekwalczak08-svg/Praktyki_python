from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class RoleEnum(str, Enum):
    """Role w konwersacjach"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


# ============= Messages =============
class MessageCreate(BaseModel):
    """Schemat do tworzenia wiadomości"""
    content: str = Field(..., min_length=1, max_length=10000, description="Zawartość wiadomości")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊"
            }
        }


class MessageRead(BaseModel):
    """Schemat do odczytywania wiadomości"""
    id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "Cześć! To moja pierwsza wiadomość z Pythona i Docker 😊",
                "created_at": "2026-03-17T09:16:11.150471"
            }
        }


# ============= Conversations =============
class ConversationCreate(BaseModel):
    """Schemat do tworzenia rekordu konwersacji"""
    session_id: str = Field(..., min_length=1, max_length=50, description="ID sesji")
    role: RoleEnum = Field(..., description="Rola: system, user lub assistant")
    content: str = Field(..., min_length=1, max_length=10000, description="Treść wiadomości")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_123abc",
                "role": "user",
                "content": "Jak się masz?"
            }
        }


class ConversationRead(BaseModel):
    """Schemat do odczytywania konwersacji"""
    id: int
    session_id: str
    role: RoleEnum
    content: str
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
