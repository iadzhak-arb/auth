from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    password: str
    remember: bool = False


class UserRegistration(UserBase):
    first_name: str
    last_name: str
    password: str


class UserPublic(UserBase):
    id: int
    first_name: str
    last_name: str
