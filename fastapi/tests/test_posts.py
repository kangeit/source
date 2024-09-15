import pytest
from app import schema

def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts")
    posts = [schema.ResponseVote(**i) for i in res.json()]
    assert res.status_code == 200
    

def test_get_post_by_id(authorized_client):
    res = authorized_client.get("/posts/22")
    post = schema.ResponseVote(**res.json())
    assert post is not None
    assert res.status_code == 200
    

def test_get_post_by_id_not_exist(authorized_client):
    res = authorized_client.get("/posts/-1")
    assert res.status_code == 404
    assert "No data found with" in res.json().get("detail") 


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts")
    assert res.status_code == 401

    

def test_unauthorized_user_get_post_by_id(client):
    res = client.get("/posts/22")
    assert res.status_code == 401



@pytest.mark.parametrize("title, content, published", 
                        [("post title 122301", "post content 122301 001", False),
                         ("post title 122302", "post content 122302 002", True)])
def test_add_post(authorized_client, test_user, title, content, published):
    payload = {"title": title,
               "content": content,
               "published": published
               }
    headers = {}
    res = authorized_client.post(url="/posts/", headers=headers, json=payload)
    post = schema.Response(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user.email == test_user['email']
    assert post.user.user_id == test_user['user_id']


@pytest.mark.parametrize("title, content", 
                        [("post title 122301", "post content 122301 001")])
def test_add_post_default_published_value(authorized_client, test_user, title, content):
    payload = {"title": title,
               "content": content,
               }
    headers = {}
    res = authorized_client.post(url="/posts/", headers=headers, json=payload)
    post = schema.Response(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == True
    assert post.user.email == test_user['email']
    assert post.user.user_id == test_user['user_id']


@pytest.mark.parametrize("title, content", 
                        [("post title 122301", "post content 122301 001")])
def test_unauthorized_user_add_post(client, title, content):
    payload = {"title": title,
               "content": content,
               }
    headers = {}
    res = client.post(url="/posts/", headers=headers, json=payload)
    assert res.status_code == 401