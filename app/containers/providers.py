from dishka import provide, Provider, Scope
from httpx import AsyncClient
from telegram import Bot

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
    def get_chat_web_service(self) -> BaseChatWebService:
        return ChatWebService(
            http_client=self.get_http_client(),
            base_url=self.get_settings().WEB_API_BASE_URL,
        )

    @provide(scope=Scope.REQUEST)
    def get_telegram_bot(self) -> Bot:
        return Bot(token=self.get_settings().TG_BOT_TOKEN)
