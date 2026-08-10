from typing import Annotated

from fastapi import APIRouter, status, Body, HTTPException

from ..dependencies import SessionDep, TokenPayloadDep
from ..schemas import UserPublic, UserUpdate, UserChangePassword
from ..services import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/me')
async def me(
        session: SessionDep,
        payload: TokenPayloadDep
) -> UserPublic | None:
    user = await UserService.get_by_id(session=session, pk=int(payload.sub))
    return user


@router.put('/me')
async def me(
        session: SessionDep,
        payload: TokenPayloadDep,
        data: UserUpdate,
) -> None:
    await UserService.change_data(
        session=session,
        pk=int(payload.sub),
        first_name=data.first_name,
        last_name=data.last_name
    )
    return None


@router.put('/change-password')
async def change_password(
    session: SessionDep,
    payload: TokenPayloadDep,
    data: UserChangePassword
) -> None:
    try:
        await UserService.change_password(
            session=session,
            pk=int(payload.sub),
            password=data.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0]
        )
    return None