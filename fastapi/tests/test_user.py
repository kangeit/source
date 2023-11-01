import pytest
import requests
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

@pytest.mark.add_user
def test_add_user():
    
    payload = {"email": "user1@test.com",
              "password": "password1"}
    headers = {}
    
    res = client.post(url="/users", headers=headers, json=payload)

    assert res.status_code == 201
    
    
    
@pytest.mark.get_user
def test_get_user():
    
    payload = {}
    headers = {}
    res = client.get(url="/users/11", headers=headers)
    data = res.json()
    print(data)
    assert data.get("user_id") is not None
    assert res.status_code == 200
