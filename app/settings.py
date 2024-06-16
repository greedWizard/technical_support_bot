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
    WEB_API_BASE_URL: str = env('WEB_API_BASE_URL', default='http://main-app:8000')
    KAFKA_BROKER_URL: str = env('KAFKA_BROKER_URL', default='kafka:29092')
    NEW_MESSAGE_TOPIC: str = env('NEW_MESSAGE_TOPIC', default='new-messages')
    KAFKA_GROUP_ID: str = env('KAFKA_GROUP_ID', default='tg-bot')


@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()
