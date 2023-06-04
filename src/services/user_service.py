from uuid import uuid4
from typing import Iterator, Sequence
import src.repositories.user_repository as repository

from src.models.user_model import User
from src.schemas.user_schemas import UserResponse




def get_users() -> Sequence[User]:
    return repository.get_all()

def get_user_by_id(user_id: int) -> User:
    return repository.get_by_id(user_id)

def create_user(user_create) -> User:
    
    return repository.add(user_create)

def delete_user_by_id(user_id: int) -> None:
    return repository.delete_by_id(user_id)
    
def login(user_credentials) -> User:
    return repository.login(user_credentials)
