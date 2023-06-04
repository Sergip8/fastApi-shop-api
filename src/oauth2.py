from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError

from src.schemas.user_schemas import TokenData
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="users/login",
    scopes={
    
        "basic_write": "write basic information",
        "basic_read": "read basic information",  
        "advance_read": "read advance information",
        "advance_write": "write advance information"
    })

SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expires_min

def create_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return token

def verify_access_token(token: str, credencials_exeption):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM,])
        user_id = payload.get("user_id") 
        email = payload.get("email")
        if not (user_id and email):
            raise credencials_exeption
        token_scopes = payload.get("scopes", [])
        print("-----------------------")
        print(token_scopes)
        token_data = TokenData(scopes=token_scopes, user_id= user_id, email= email)
        return token_data
    except (JWTError, ValidationError):
        raise credencials_exeption
   
       
    
def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth_scheme)],):
    
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credencials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="no se pudo autenticar el usuario", headers={"WWW-Authenticate": authenticate_value})
    token_data = verify_access_token(token, credencials_exeption)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="no tiene permiso para efectuar esta acción",
                                headers={"WWW-Authenticate": authenticate_value})

    return token_data


    