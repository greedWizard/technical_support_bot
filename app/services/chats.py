from dataclasses import dataclass

from dtos.messages import ChatInfoDTO
from exceptions.chats import ChatAlreadyExistsError, ChatNotFoundByTelegramIDError
from repositories.chats.base import BaseChatsRepository


@dataclass(eq=False)
class ChatsService:
    repository: BaseChatsRepository

    async def add_chat(self, telegram_chat_id: str, web_chat_id: str) -> ChatInfoDTO:
        if await self.repository.check_chat_exists(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatAlreadyExistsError(
                telegram_chat_id=telegram_chat_id,
                web_chat_id=web_chat_id,
            )

        return await self.repository.add_chat(chat_info=ChatInfoDTO(
            web_chat_id=web_chat_id,
            telegram_chat_id=telegram_chat_id,
        ))

    async def get_chat_info_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        if await self.repository.check_chat_exists(
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatNotFoundByTelegramIDError(telegram_chat_id=telegram_chat_id)

        return await self.repository.get_by_telegram_id(telegram_chat_id=telegram_chat_id)
