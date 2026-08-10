from datetime import timedelta

from authx import AuthX, AuthXConfig

from settings import config

auth_config = AuthXConfig(
    JWT_SECRET_KEY=config.SECRET_KEY,
    JWT_TOKEN_LOCATION=['cookies'],
    JWT_COOKIE_CSRF_PROTECT=False,
    JWT_COOKIE_HTTP_ONLY=True,
    JWT_COOKIE_SECURE=False,
    JWT_COOKIE_SAMESITE='lax',
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    ),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(
        minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES
    )
)

auth = AuthX(config=auth_config)
