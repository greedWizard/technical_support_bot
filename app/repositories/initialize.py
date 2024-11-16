import sqlite3

from repositories.sqls import CREATE_MAPPING_TABLE_SQL_QUERY
from settings import get_settings


def create_tables():
    settings = get_settings()

    with sqlite3.connect(database=settings.DATABASE_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_MAPPING_TABLE_SQL_QUERY)
