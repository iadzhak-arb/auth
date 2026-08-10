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
    # JWT
    SECRET_KEY: str = 'secret_key'  # use to generate: openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    # DB
    DB_URL: str = Field('sqlite+aiosqlite:///database.db', alias='AUTH_DB_URL')

    # CORS
    ALLOWED_HOSTS: list[str] = DEFAULT_ALLOWED_HOSTS


config = Config()
