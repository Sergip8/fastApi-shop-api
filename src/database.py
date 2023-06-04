from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'
SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test'    
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine_test = create_engine(SQLALCHEMY_DATABASE_URL_TEST, echo=True)
SessionLocal = sessionmaker(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()