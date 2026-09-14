from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


Role = Literal["user", "assistant"]


class Message(BaseModel):
    role: Role
    text: str = Field(..., min_length=1, max_length=20000)
    timestamp: datetime


class SendMessageRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class ChatCreateResponse(BaseModel):
    chat_id: str


class ChatMessageResponse(BaseModel):
    chat_id: str
    message: Message


class ChatCloseResponse(BaseModel):
    message: str
    rank: int = Field(..., ge=1, le=10)


class ChatResponse(BaseModel):
    chat_id: str
    user_id: str
    messages: List[Message]
    is_closed: bool
    rank_generated: bool
    created_at: datetime
    closed_at: Optional[datetime] = None
