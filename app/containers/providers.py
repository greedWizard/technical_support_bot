from dishka import provide, Provider, Scope, AnyOf
from httpx import AsyncClient
from telegram import Bot

from repositories.chats.base import BaseChatsRepository, SQLChatsRepository
from services.chats import ChatsService
from services.web import BaseChatWebService, ChatWebService
from settings import ProjectSettings


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> ProjectSettings:
        return ProjectSettings()

    @provide(scope=Scope.REQUEST)
    def get_http_client(self) -> AsyncClient:
        return AsyncClient()

    @provide(scope=Scope.REQUEST)
    def get_chat_web_service(self, settings: ProjectSettings, http_client: AsyncClient) -> AnyOf[BaseChatWebService, ChatWebService]:
        return ChatWebService(
            http_client=http_client,
            base_url=settings.WEB_API_BASE_URL,
        )

    @provide(scope=Scope.REQUEST)
    def get_telegram_bot(self, settings: ProjectSettings) -> Bot:
        return Bot(token=settings.TG_BOT_TOKEN)

    @provide(scope=Scope.REQUEST)
    def get_chats_repository(self, settings: ProjectSettings) -> AnyOf[BaseChatsRepository, SQLChatsRepository]:
        return SQLChatsRepository(database_url=settings.DATABASE_NAME)

    @provide(scope=Scope.REQUEST)
    def get_chats_service(self, repository: BaseChatsRepository) -> ChatsService:
        return ChatsService(repository=repository)
