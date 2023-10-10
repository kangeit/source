import pytest
import requests



@pytest.mark.add_user
def test_add_user():
    
    payload = {"email": "user1@test.com",
              "password": "password1"}
    headers = {}
    
    response = requests.post(url="http://127.0.0.1:8000/users", headers=headers, json=payload)
    print(response)
    assert response.status_code == 201
    
    
    
@pytest.mark.get_user
def test_add_user():
    
    payload = {}
    headers = {}
    response = requests.get(url="http://127.0.0.1:8000/users/11", headers=headers, json=payload)
    
    data = response.json()
    print(data["user_id"])
    assert data["user_id"] is not None
    assert response.status_code == 200
