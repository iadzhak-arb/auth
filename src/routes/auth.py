from datetime import timedelta

from fastapi import APIRouter, HTTPException, Response, status

from ..auth import auth
from ..dependencies import SessionDep, TokenPayloadRefreshDep
from ..schemas import UserLogin, UserPublic, UserRegistration
from ..services import UserService
from ..settings import config

router = APIRouter(tags=["auth"])


@router.post('/login')
async def login(
        data: UserLogin,
        response: Response,
        session: SessionDep
) -> None:
    user = await UserService.authenticate(
        session=session,
        email=data.email,
        password=data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Некорректная почта и/или пароль'
        )
    token = auth.create_access_token(uid=str(user.id))
    if data.remember:
        refresh = auth.create_refresh_token(uid=str(user.id))
    else:
        refresh = auth.create_refresh_token(
            uid=str(user.id),
            expiry=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES * 2)
        )

    auth.set_access_cookies(token, response)
    auth.set_refresh_cookies(refresh, response)

    return None


@router.post('/registration')
async def registration(
        data: UserRegistration,
        session: SessionDep
) -> UserPublic | None:
    try:
        user = await UserService.register(
            session=session,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0]
        )


@router.post('/logout')
async def logout(response: Response):
    auth.unset_cookies(response)
    return None


@router.get('/refresh')
async def refresh(payload: TokenPayloadRefreshDep, response: Response):
    access_token = auth.create_access_token(uid=payload.sub, fresh=False)
    refresh_token = auth.create_refresh_token(uid=payload.sub)
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)
    return None
