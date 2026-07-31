from authx import AuthX, AuthXConfig

from settings import config


auth_config = AuthXConfig(
    JWT_SECRET_KEY=config.SECRET_KEY,
    JWT_TOKEN_LOCATION=['cookies']
)
auth = AuthX(config=auth_config)

