from fastapi import APIRouter

from ..dependencies import SessionDep, TokenPayloadDep
from ..schemas import UserPublic
from ..services import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/me')
async def me(
        session: SessionDep,
        payload: TokenPayloadDep
) -> UserPublic | None:
    user = await UserService.get_by_id(session=session, pk=int(payload.sub))
    return user
