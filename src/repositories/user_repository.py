from contextlib import AbstractContextManager
from typing import Callable, Iterator, Optional, Sequence
from fastapi import Depends
from sqlalchemy import select
from src.database import SessionLocal
from src.utils import hash, verify
from src.database import  Session
from src.models.user_model import User
from src.schemas.user_schemas import UserCreate, UserResponse
from src.oauth2 import create_token



def get_all() -> Sequence[User]:
    with SessionLocal() as session:
         return session.scalars(select(User)).all()

def get_by_id(user_id: int) -> User:
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            raise Exception
        return user

def add(user_create: UserCreate,) -> User:
    with SessionLocal() as session:
        user_create.password = hash(user_create.password)
        user = User(**user_create.dict())
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        
    except:
        raise Exception
    return user

def delete_by_id(user_id: int) -> None:
    with SessionLocal() as session:
        entity: Optional[User] = session.get(User, user_id)
        if not entity:
            raise Exception
        session.delete(entity)
        session.commit()

def login(user_credentials):
    with SessionLocal() as session:
        entity: Optional[User] = session.query(User).filter(User.email == user_credentials.username ).first()
         
        if not entity or not verify(entity.password, user_credentials.password):
            raise Exception
        
        token_response = create_token({"user_id": entity.id, "email": entity.email})
        return {"access_token": token_response, "token_type": "bearer"}








