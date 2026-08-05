from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # JWT
    SECRET_KEY: str = 'secret_key'  # use to generate: openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    # DB
    DB_URL: str = 'sqlite+aiosqlite:///database.db'

    # CORS
    ALLOWED_HOSTS: list[str] = [
        'http://localhost:5173',
        'http://127.0.0.1:8001',
        'http://localhost:8001',
        'http://localhost',
        'http://192.168.0.100'
    ]


config = Config()
