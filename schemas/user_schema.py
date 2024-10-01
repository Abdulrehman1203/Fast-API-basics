from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None


class TokenRequest(BaseModel):
    token: str
