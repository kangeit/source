import psycopg
import pytest
from fastapi.testclient import TestClient
from app.main import app
from psycopg.rows import dict_row
from app.config import settings


@pytest.fixture(scope="module")
def client():
    # do action before the test
    yield TestClient(app)
    # do action after the test
 
    
@pytest.fixture()
def db_conn():
    with psycopg.connect(
            host=settings.database_hostname, 
            dbname=settings.database_name,
            user=settings.database_username, 
            password=settings.database_password
        ) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            yield cursor

    
@pytest.fixture(scope="module")
def test_user(client):
    test_user_data = {"email": "user12192@xxgmail.com",
                      "password": "pwd1"}
    
    res = client.post(url="/users", json=test_user_data)
    user = res.json()
    user["password"] = test_user_data["password"]
    assert res.status_code == 201
    print(user)
    return user

