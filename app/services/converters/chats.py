from datetime import datetime
from dtos.mesages import ChatListItemDTO, ChatListenerDTO


def convert_chat_response_to_chat_dto(chat_data: dict) -> ChatListItemDTO:
    return ChatListItemDTO(
        oid=chat_data['oid'],
        title=chat_data['title'],
        created_at=datetime.fromisoformat(chat_data['created_at']),
    )


def convert_chat_listener_response_to_listener_dto(listener_data: dict) -> ChatListenerDTO:
    return ChatListenerDTO(oid=listener_data['oid'])
