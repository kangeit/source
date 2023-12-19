from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import schema, database, oauth2
from typing import List, Optional, Annotated

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[schema.ResponseVote])
def get_posts(current_user: schema.UserResp = Depends(oauth2.get_current_user),
              limit: int = 4, search_content: Optional[str] = ""):

    posts_query = """select p.post_id, p.title, p.content, p.published, p.user_id, 
                         count(v.post_id) as votes 
                         from posts p left join votes v 
                         on p.post_id = v.post_id 
                         where content like '%%' || %s || '%%' 
                         group by p.post_id limit %s"""
    posts_params = (search_content, limit)
    posts = database.execute_sql_query(posts_query, *posts_params)

    users_query = """select * from users"""
    user_data = database.execute_sql_query(users_query)

    for post in posts:
        for user in user_data:
            if post['user_id'] == user['user_id']:
                post['user'] = user
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.Response)
def create_posts(post: schema.Post, current_user: Annotated[schema.UserResp, Depends(oauth2.get_current_user)]):
    
    query = """insert into posts (title, content, published, user_id)
            values (%s, %s, %s, %s) returning *"""
    params = (post.title, post.content, post.published, current_user["user_id"])
    new_posts = database.execute_sql_query(query, *params)
    data = new_posts[0]
    data['user'] = current_user
    return data


@router.get("/{post_id}", response_model=schema.ResponseVote)
def get_post(post_id: int, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    post_query = """select p.post_id, p.title, p.content, p.published, p.user_id, 
                         count(v.post_id) as votes 
                         from posts p left join votes v 
                         on p.post_id = v.post_id 
                         where p.post_id = %s 
                         group by p.post_id"""
    post_params = (post_id,)
    post = database.execute_sql_query(post_query, *post_params)[0]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with {post_id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"No data found with {book_id}"}
    user_data = database.execute_sql_query("""select * from users where user_id = %s""", *(post['user_id'],))[0]
    post['user'] = user_data
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    post_query = """select * from posts where post_id = %s"""
    delete_post_query = """delete from posts where post_id = %s returning *"""    
    post = database.execute_sql_query(post_query, *(post_id,))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post is {post_id}")

    if post[0]["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action To Delete Post")
    else:
        database.execute_sql_query(delete_post_query, *(post_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schema.Response)
def update_post(post_id: int, post: schema.Post, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    query = """select * from posts where post_id = %s"""
    update_query = """update posts set title = %s, content = %s, published = %s where post_id = %s returning *"""
    params = (post_id,)
    update_params = (post.title, post.content, post.published, post_id)
    post = database.execute_sql_query(query, *params)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no book id {post_id}")

    if post[0]["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action To Update Post")
    else:
        post = database.execute_sql_query(update_query, *update_params)
        
    post[0]['user'] = current_user    
    return post[0]
