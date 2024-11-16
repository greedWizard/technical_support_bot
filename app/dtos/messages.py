from datetime import datetime
from pydantic import BaseModel


class ChatListItemDTO(BaseModel):
    oid: str
    title: str
    created_at: datetime


class ChatListenerDTO(BaseModel):
    oid: str


class ChatInfoDTO(BaseModel):
    telegram_chat_id: str
    web_chat_id: str
