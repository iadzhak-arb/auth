from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import config

from .error_handlers import register_error_handlers
from .routes import auth_router, user_router

app = FastAPI(
    root_path='/api/auth',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)
app.include_router(user_router)
register_error_handlers(app)
