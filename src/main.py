from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import config
from .auth import auth
from .routes import router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
auth.handle_errors(app)
