from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Literal
from pydantic.types import conint

class POST(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(POST):
    pass


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config():
        orm_mode =  True

class PostResponse(POST):
    id: int
    user_id: int
    user: UserResponse
    created_at: datetime


    class Config():
        orm_mode =  True



class PostOut(BaseModel):
    votes: int
    Post: PostResponse
    # title: str
    # content: str
    # id: int
    # user_id: int
    # published: bool
    # user: UserResponse
    # created_at: datetime

    class Config():
        orm_mode =  True


class PostUser(UserBase):
    password: str
    
class LoginUser(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None

class VoteBase(BaseModel):
    post_id: int
    dir: Literal[0, 1]

    @field_validator("dir")
    def validate_dir(cls, value):
        if value not in (0, 1):
            raise ValueError("dir must be either 0 (downvote) or 1 (upvote)")
        return value