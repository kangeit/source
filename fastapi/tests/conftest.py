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
    
    
@pytest.fixture(scope="module")
def test_user(client):
    test_user_data = {"email": "testuser@test.com",
                      "password": "password1"}
    
    res = client.post(url="/users", json=test_user_data)
    user = res.json()
    user["password"] = test_user_data["password"]
    assert res.status_code == 201
    return user

try:
    conn = psycopg.connect(host=settings.database_hostname, dbname=settings.database_name,
                           user=settings.database_username, password=settings.database_password)
    # conn = psycopg.connect(host="localhost", dbname="pgdb", user="postg_dev", password="postgres")
    cur = conn.cursor(row_factory=dict_row)
except Exception as e:
    print("Database error", e)