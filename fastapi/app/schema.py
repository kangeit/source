from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class Post(PostBase):
    pass


class UserResp(BaseModel):
    user_id: int
    email: EmailStr
    create_date: datetime

    class Config:
        orm_mode = True


class Response(PostBase):
    post_id: int
    user: UserResp

    class Config:
        orm_mode = True


class ResponseVote(PostBase):
    post_id: int
    votes: int
    user: UserResp

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        orm_mode = True
