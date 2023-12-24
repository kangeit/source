import psycopg
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schema
from jose import jwt
from psycopg.rows import dict_row
from app.config import settings
from app.oauth2 import create_access_token

@pytest.fixture()
def client():
    # do action before the test
    yield TestClient(app)
    # do action after the test
 
    
@pytest.fixture(scope="session")
def db_conn():
    with psycopg.connect(
            host=settings.database_hostname, 
            dbname=settings.database_name,
            user=settings.database_username, 
            password=settings.database_password
        ) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            yield cursor

    
@pytest.fixture()
def test_user(client):
    # test_user_data = {"email": "user1220@xxgmail.com",
    #                   "password": "pwd1"}    
    res = client.get(url="/users/38")
    user = res.json()    
    assert res.status_code == 200
    return user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["user_id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    yield client