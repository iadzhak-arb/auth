from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserORM
from ..schemas import UserPublic
from .password_validators import password_validator
from .security import get_password_hash, verify_password


class UserService:
    @classmethod
    async def authenticate(
            cls,
            session: AsyncSession,
            email: str,
            password: str
    ) -> UserPublic | None:
        stmt = select(UserORM).filter_by(email=email)
        result = await session.execute(stmt)
        user: UserORM | None = result.scalars().first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return UserPublic.model_validate(user)

    @classmethod
    async def register(
            cls,
            session: AsyncSession,
            email: str,
            password: str,
            first_name: str | None = None,
            last_name: str | None = None,
    ) -> UserPublic | None:
        errors = {}
        stmt = select(UserORM).filter_by(email=email)
        result = await session.execute(stmt)
        if result.scalars().first():
            errors['email'] = 'Email already registered'
        password_validation = password_validator.evaluate(
            password,
            context_data={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if not password_validation.valid:
            errors['password'] = ' '.join([
                i.message
                for i in password_validation.issues
            ])
        if errors:
            raise ValueError(errors)

        user = UserORM(
            email=email,
            hashed_password=get_password_hash(password)
        )
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        session.add(user)
        await session.commit()
        return UserPublic.model_validate(user)

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        pk: int
    ) -> UserPublic | None:
        stmt = select(UserORM).filter_by(id=pk)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return UserPublic.model_validate(user) if user else None

    @classmethod
    async def change_data(
            cls,
            session: AsyncSession,
            pk: int,
            first_name: str | None = None,
            last_name: str | None = None,
    ) -> None:
        stmt  =select(UserORM).filter_by(id=pk)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        await session.commit()

    @classmethod
    async def change_password(
        cls,
        session: AsyncSession,
        pk: int,
        password: str
    ) -> None:
        stmt = select(UserORM).filter_by(id=pk)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise ValueError('User not found')
        errors = {}
        password_validation = password_validator.evaluate(
            password,
            context_data={
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        )
        if not password_validation.valid:
            errors['password'] = ' '.join([
                i.message
                for i in password_validation.issues
            ])
        if errors:
            raise ValueError(errors)
        user.hashed_password = get_password_hash(password)
        await session.commit()
