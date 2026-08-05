from typing import Annotated

from authx import TokenPayload
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import auth
from .database import get_session

AuthDep = Depends(auth.access_token_required)
TokenPayloadDep = Annotated[TokenPayload, Depends(auth.access_token_required)]
TokenPayloadRefreshDep = Annotated[
    TokenPayload,
    Depends(auth.refresh_token_required)
]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
