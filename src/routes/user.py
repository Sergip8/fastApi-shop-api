from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from src.models.user_model import Permissions, User
from src.oauth2 import create_token
from src.schemas.user_schemas import UserCreate, UserPermissionsResponse, UserResponse
from src.schemas.user_schemas import UserCreate, UserResponse

from sqlalchemy.orm import Session, joinedload
from src.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from src.utils import hash, verify

router = APIRouter()

router = APIRouter(prefix="/users", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["users"])

    
@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[UserResponse])
def get_list(session: Session = Depends(get_db)):

    return session.scalars(select(User)).all()
 

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)

def get_by_id(user_id: int, session: Session = Depends(get_db)):
    try:
        return session.get(User, user_id)
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= UserPermissionsResponse)

def Register(user_create: UserCreate, session: Session = Depends(get_db)):
    user_create.password = hash(user_create.password)
    user_p = user_create.dict()
    p = user_p.pop("permissions")
    user = User(**user_p)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        permission = Permissions(permissions=p, user_id=user.id)
        session.add(permission)
        session.commit()
        user_permissions = session.scalars(
            select(User)
            .options(joinedload(User.permissions))
            .filter_by(id=user.id)
        ).first() 
        return user_permissions 
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="el email ya existe")

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    try:
        user = session.scalars(
            select(User)
            .options(joinedload(User.permissions))
            .filter_by(email= user_credentials.username)
        ).first() 
        if not user or not verify(user.password, user_credentials.password):
            raise Exception
    except Exception:
        return Response(status_code=status.HTTP_403_FORBIDDEN, content="email o password incorrectos")
    token_response = create_token({"user_id": user.id, "email": user.email, "scopes": user.permissions.permissions})
    return {"access_token": token_response, "token_type": "bearer"}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)

def remove(user_id: int, session: Session = Depends(get_db)):
    try:
            user = session.get(User, user_id)
    except Exception:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario")
    session.delete(user)
    session.commit()


