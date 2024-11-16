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
    def message(self):
        return 'Не удалось получить список всех чатов.'


@dataclass(frozen=True, eq=False)
class ListenerListRequestError(BaseWebException):
    @property
    def message(self):
        return 'Не удалось получить список всех слушателей чата.'


@dataclass(frozen=True, eq=False)
class ListenerAddRequestError(BaseWebException):
    @property
    def message(self):
        return 'Не удалось добавить слушателя к чату.'


@dataclass(frozen=True, eq=False)
class ChatAlreadyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return 'Чат с такими данными уже существует'


@dataclass(frozen=True, eq=False)
class ChatInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return 'Не удалось найти созданный чат'


@dataclass(frozen=True, eq=False)
class ChatInfoRequestError(BaseWebException):
    @property
    def message(self):
        return 'Не удалось получить информацию о чате.'
