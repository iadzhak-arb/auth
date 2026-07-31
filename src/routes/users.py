from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body, Response
from authx import TokenPayload
from sqlalchemy import select

from ..auth import auth
from ..dependencies import SessionDep
from ..models import User, UserPublic, UserIn
from ..security import verify_password


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post('/registration', response_model=UserPublic)
async def registration(user: UserIn, session: SessionDep):
    stmt = select(User).filter_by(email=user.email)
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{
                "field": "email",
                "message":"Email already registered"
            }]
        )
    user.hash_password()
    user = User.model_validate(user)
    session.add(user)
    await session.commit()
    return user


@router.post('/login')
async def login(
        email: Annotated[str, Body()],
        password: Annotated[str, Body()],
        session: SessionDep,
        response: Response,
):
    stmt = select(User).filter_by(email=email)
    result = await session.execute(stmt)
    user: User | None = result.scalars().first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Некорректная почта и/или пароль'
        )
    token = auth.create_access_token(uid=str(user.id))
    refresh = auth.create_refresh_token(uid=str(user.id))
    auth.set_access_cookies(token, response)
    auth.set_refresh_cookies(refresh, response)
    return 'ok'


@router.post('/logout')
async def logout(response: Response):
    auth.unset_cookies(response)
    return 'logout'


@router.get('/me', response_model=UserPublic)
async def me(
        payload: Annotated[TokenPayload, Depends(auth.access_token_required)],
        session: SessionDep,
):
    stmt = select(User).filter_by(id=int(payload.sub))
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


@router.get('/refresh')
async def refresh(
payload: Annotated[TokenPayload, Depends(auth.access_token_required)],
        session: SessionDep,
        response: Response,
):
    stmt = select(User).filter_by(id=int(payload.sub))
    result = await session.execute(stmt)
    user = result.scalars().first()
    token = auth.create_access_token(uid=str(user.id))
    refresh = auth.create_refresh_token(uid=str(user.id))
    auth.set_access_cookies(token, response)
    auth.set_refresh_cookies(refresh, response)
    return 'ok'