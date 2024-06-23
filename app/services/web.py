from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient

from dtos.mesages import ChatListItemDTO, ChatListenerDTO
from exceptions.chats import (
    ChatInfoRequestError,
    ChatListRequestError,
    ListenerAddRequestError,
    ListenerListRequestError,
)
from services.constants import CHAT_INFO_URI, CHAT_LIST_URI, CHAT_LISTENERS_URI, DEFAULT_LIMIT, DEFAULT_OFFSET
from services.converters.chats import convert_chat_listener_response_to_listener_dto, convert_chat_response_to_chat_dto


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        ...

    @abstractmethod
    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        ...

    @abstractmethod
    async def add_listener(self, telegram_chat_id: int, chat_oid: str):
        ...

    @abstractmethod
    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO:
        ...


@dataclass
class ChatWebService(BaseChatWebService):
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LIST_URI),
            params={'limit': DEFAULT_LIMIT, 'offset': DEFAULT_OFFSET}
        )

        if not response.is_success:
            raise ChatListRequestError(status_code=response.status_code, response_content=response.content.decode())

        json_data = response.json()
        return [convert_chat_response_to_chat_dto(chat_data=chat_data) for chat_data in json_data['items']]

    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid)),
        )

        if not response.is_success:
            raise ListenerListRequestError(status_code=response.status_code, response_content=response.content.decode())

        json_data = response.json()
        return [convert_chat_listener_response_to_listener_dto(
            listener_data=listener_data) for listener_data in json_data
        ]

    async def add_listener(self, telegram_chat_id: int, chat_oid: str) -> None:
        response = await self.http_client.post(
            url=urljoin(
                base=self.base_url,
                url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid),
            ),
            json={'telegram_chat_id': str(telegram_chat_id)}
        )

        if not response.is_success:
            raise ListenerAddRequestError(status_code=response.status_code, response_content=response.content.decode())

    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO:
        response = await self.http_client.get(
            url=urljoin(
                base=self.base_url,
                url=CHAT_INFO_URI.format(chat_oid=chat_oid),
            ),
        )

        if not response.is_success:
            raise ChatInfoRequestError(status_code=response.status_code, response_content=response.content.decode())

        return convert_chat_response_to_chat_dto(chat_data=response.json())
