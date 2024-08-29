from pydantic import BaseModel, ConfigDict, EmailStr

from mada.models import LivroState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class LivroSchema(BaseModel):
    title: str
    description: str
    ano: str
    autor: str
    state: LivroState


class LivroPublic(LivroSchema):
    id: int


class LivroList(BaseModel):
    livros: list[LivroPublic]


class LivroUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: LivroState | None = None
