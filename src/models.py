from datetime import datetime, timezone

from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel

from .security import get_password_hash
from .validators import password_validator


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    first_name: str | None = Field(max_length=50)
    last_name: str | None = Field(max_length=50)

class UserIn(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v, info):
        password_validator(v, info)
        return v

    def hash_password(self, hash_fn = get_password_hash) -> None:
        self.password = hash_fn(self.password)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default=datetime.now(timezone.utc))


class UserPublic(UserBase):
    id : int
