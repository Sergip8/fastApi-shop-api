

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    
    pass


class User(BaseModel):
    email: EmailStr
    

class UserCreate(User):
    password: str
    permissions: List[str]

class Permssion(BaseModel):
     permissions: List[str]
     class Config:
        orm_mode = True

class UserResponse(User):
    id: int
    
    #created_at: datetime
    class Config:
        orm_mode = True

class UserPermissionsResponse(UserResponse):
    permissions: Permssion

class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
     email: str
     password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    scopes: list[str] = []

class Vote(BaseModel):
    post_id:int
    #dir: conint(le=1)