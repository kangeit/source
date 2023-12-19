from jose import jwt
import pytest
from app import schema
from app.config import settings


@pytest.mark.add_user
def test_add_user(client):
    
    payload = {"email": "user1101@test.com",
               "password": "password1"}
    headers = {}
    
    res = client.post(url="/users", headers=headers, json=payload)

    assert res.status_code == 201
    
    
    
@pytest.mark.get_user
def test_get_user(client):
    
    payload = {}
    headers = {}
    res = client.get(url="/users/11", headers=headers)
    user_data = schema.UserResp(**res.json())  
    
    assert user_data.user_id is not None
    assert res.status_code == 200


@pytest.mark.login_user
def test_login_user(client, test_user):
    
    payload = {"username": test_user["email"],
              "password": test_user["password"]}
    headers = {}
    res = client.post(url="/login", headers=headers, data=payload)
    user_data = schema.Token(**res.json())
    data = jwt.decode(user_data.access_token, settings.secret_key, algorithms=settings.algorithm)
    assert user_data.token_type == "bearer"
    assert test_user["user_id"] == data.get("user_id")
    assert res.status_code == 200