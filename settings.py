from functools import lru_cache
import environ

from pydantic_settings import BaseSettings


env = environ.Env()
environ.Env.read_env('.env')


class ProjectSettings(BaseSettings):
    TG_BOT_TOKEN: str = env('TG_BOT_TOKEN')
    GREETING_TEXT: str = env(
        'GREETING_TEXT',
        default=(
                'Добро пожаловать в бот техподдержки.\n'
                'Пожалуйста выберите чат для работы с клиентом.\nПолучить список всех чатов: '
                '/chats, выбрать чат /set_chats <oid чата>.'
        ),
    )
    WEB_API_BASE_URL: str = env('WEB_API_BASE_URL', default='http://localhost:8000')


@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()
