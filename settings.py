from pydantic_settings import BaseSettings

class Config(BaseSettings):
    SECRET_KEY: str = 'secret_key'  # use to generate: openssl rand -hex 32
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_URL: str = f'sqlite+aiosqlite:///database.db'
    ALLOWED_HOSTS: list[str] = ['http://localhost:5173', 'http://127.0.0.1:8000', 'http://localhost:8000']

config = Config()