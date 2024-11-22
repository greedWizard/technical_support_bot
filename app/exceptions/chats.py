from dataclasses import dataclass
import json

from exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get('detail', {}).get('error', '')


@dataclass(frozen=True, eq=False)
class ChatListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить список всех чатов.'


@dataclass(frozen=True, eq=False)
class ListenerListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить список всех слушателей чата.'


@dataclass(frozen=True, eq=False)
class ListenerAddRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось добавить слушателя к чату.'


@dataclass(frozen=True, eq=False)
class ChatAlreadyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Чат с такими данными уже существует'


@dataclass(frozen=True, eq=False)
class ChatInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Не удалось найти созданный чат'


@dataclass(frozen=True, eq=False)
class ChatNotFoundByTelegramIDError(ApplicationException):
    telegram_chat_id: str

    @property
    def message(self) -> str:
        return 'Чат для ответа не зарегистрирован в боте.'


@dataclass(frozen=True, eq=False)
class ChatInfoRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Не удалось получить информацию о чате.'


@dataclass(frozen=True, eq=False)
class SendMessageToChatError(ApplicationException):
    @property
    def message(self) -> str:
        return 'Не удалось отправить сообщение в чат.'
