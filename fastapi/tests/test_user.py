import pytest
from app import schema
from jose import jwt
from app.config import settings


@pytest.mark.parametrize("email, password, status_code",
                         [('user12191@xxgmail.com', 'pwd2', 403),
                          ('user@xxgmail.com', 'pwd1', 403),
                          ('user@xxgmail.com', 'pwd2', 403),
                          ('user@xxgmail.com', None, 422),
                          (None, 'pwd2', 422)])
def test_login_fail(client, email, password, status_code):
    
    payload = {"username": email,
              "password": password}
    headers = {}
    res = client.post(url="/login", headers=headers, data=payload)
    assert res.status_code == status_code

    

def test_login_user(client):    
    payload = {"username": "user12191@xxgmail.com",
              "password": "pwd1"}
    headers = {}
    res = client.post(url="/login", headers=headers, data=payload)
    user_data = schema.Token(**res.json())
    data = jwt.decode(user_data.access_token, settings.secret_key, algorithms=settings.algorithm)
    assert user_data.token_type == "bearer"
    assert data.get("user_id") is not None
    assert res.status_code == 200