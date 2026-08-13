from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

DEFAULT_ALLOWED_HOSTS = [
        'http://localhost:5173',
        'http://127.0.0.1:8001',
        'http://localhost:8001',
        'http://localhost',
        'http://192.168.0.100'
    ]


class Config(BaseSettings):
    # CORS
    ALLOWED_HOSTS: list[str] = DEFAULT_ALLOWED_HOSTS

    # JWT
    SECRET_KEY: str = 'secret_key'  # use to generate: openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    JWT_COOKIE_SECURE: bool = False

    # DB
    DB_TYPE: Literal['sqlite', 'postgres'] = Field('sqlite', alias='AUTH_DB_TYPE')
    SQLITE_PATH: str = Field('database.db', alias='AUTH_SQLITE_PATH')
    DB_USER: str = Field('postgres', alias='AUTH_DB_USER')
    DB_PASS: str = Field('postgres', alias='AUTH_DB_PASS')
    DB_HOST: str = Field('postgres', alias='AUTH_DB_HOST')
    DB_PORT: int = Field(5432, alias='AUTH_DB_PORT')

    @property
    def db_url(self) -> str:
        if self.DB_TYPE == 'sqlite':
            return f'sqlite+aiosqlite:///{self.SQLITE_PATH}'
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}'


config = Config()
