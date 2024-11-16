from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiosqlite import connect

from dtos.messages import ChatInfoDTO
from exceptions.chats import ChatInfoNotFoundError
from repositories.sqls import ADD_NEW_CHAT_INFO, GET_CHAT_INFO_BY_TELEGRAM_ID, GET_CHAT_INFO_BY_WEB_ID, GET_CHATS_COUNT


class BaseChatsRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        ...

    @abstractmethod
    async def check_chat_exists(
        self,
        web_chat_id: str | None,
        telegram_chat_id: str | None,
    ) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        ...


@dataclass(eq=False)
class SQLChatsRepository(BaseChatsRepository):
    database_url: str

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        async with connect(self.database_url) as connection:
            await connection.execute_insert(
                ADD_NEW_CHAT_INFO,
                (chat_info.web_chat_id, chat_info.telegram_chat_id)
            )
            await connection.commit()

        return ChatInfoDTO(
            web_chat_id=chat_info.web_chat_id,
            telegram_chat_id=chat_info.telegram_chat_id,
        )

    async def get_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        async with connect(self.database_url) as connection:
            result = await connection.execute_insert(
                GET_CHAT_INFO_BY_TELEGRAM_ID,
                (telegram_chat_id,)
            )

        if result is None:
            raise ChatInfoNotFoundError(telegram_chat_id=telegram_chat_id)

        return ChatInfoDTO(
            telegram_chat_id=result[0],
            web_chat_id=result[1],
        )

    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        async with connect(self.database_url) as connection:
            result = await connection.execute_insert(
                GET_CHAT_INFO_BY_WEB_ID,
                (web_chat_id,)
            )

        if result is None:
            raise ChatInfoNotFoundError(web_chat_id=web_chat_id)

        return ChatInfoDTO(
            telegram_chat_id=result[0],
            web_chat_id=result[1],
        )

    async def check_chat_exists(
        self,
        web_chat_id: str | None,
        telegram_chat_id: str | None,
    ) -> bool:
        async with connect(self.database_url) as connection:
            result = await connection.execute_insert(
                GET_CHATS_COUNT,
                (web_chat_id, telegram_chat_id)
            )

        if result is None:
            return False

        return result[0] > 0