from fastapi.testclient import TestClient
import pytest
from src.application import app
from src.models import user_model
from src.schemas import user_schemas
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import engine_test

from psycopg2.extras import RealDictCursor 
import psycopg2
from src.config import settings
from alembic import command
from alembic.config import Config




def test_create_user(client):
  res = client.post("/users/", json={"email": "xfg@ff.com", "password": "1234", "permissions":["basic_write","basic_read",]})
  new_user = user_schemas.UserResponse(**res.json())
  assert res.status_code == 201
  assert new_user.email == "xfg@ff.com"

def test_login_user(client, test_user):
    res = client.post("/users/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = user_schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm,])
    user_id = payload.get("user_id") 
    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status",[
   ("oduibnodnhb@digdpoing.com", "slifdnglg", 403),
   ("odudnhb@digdpoing.com", "fdnglg", 403),
   ("oduibn@digdpoing.com", "sdnglg", 403),
   (None, "slinglg", 422),
   ("bnodnhb@digdpoing.com", None, 422),

])
def test_incorret_login(test_user, client, email, password, status):
   res =client.post("/users/login/", data={"username": email, "password": password})

   assert res.status_code == status
   