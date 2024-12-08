from datetime import datetime
from pydantic import BaseModel


class NewChatMessageSchema(BaseModel):
    event_id: str
    occurred_at: str
    message_text: str
    message_oid: str
    chat_oid: str


class NewChatSchema(BaseModel):
    chat_oid: str
    chat_title: str


class DeleteChatSchema(BaseModel):
    chat_oid: str
    occurred_at: datetime
