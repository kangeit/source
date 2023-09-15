from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import schema, database, oauth2
from typing import List, Optional, Annotated

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=List[schema.ResponseVote])
def get_posts(current_user: schema.UserResp = Depends(oauth2.get_current_user),
              limit: int = 4, search_content: Optional[str] = ""):
    database.cur.execute("""select p.post_id, p.title, p.content, p.published, p.user_id, 
                         count(v.post_id) as votes 
                         from posts p left join votes v 
                         on p.post_id = v.post_id 
                         where content like '%%' || %s || '%%' 
                         group by p.post_id limit %s""",
                         (search_content, limit))
    posts = database.cur.fetchall()

    database.cur.execute("""select * from users""")
    user_data = database.cur.fetchall()

    for post in posts:
        for user in user_data:
            if post['user_id'] == user['user_id']:
                post['user'] = user
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schema.Response)
def create_posts(post: schema.Post, current_user: Annotated[schema.UserResp, Depends(oauth2.get_current_user)]):

    database.cur.execute("""insert into posts (title, content, published, user_id) 
    values (%s, %s, %s, %s) returning *""", (post.title, post.content, post.published, current_user["user_id"]))

    new_posts = database.cur.fetchone()
    database.conn.commit()
    new_posts['user'] = current_user
    return new_posts


@router.get("/{post_id}", response_model=schema.ResponseVote)
def get_post(post_id: int, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    database.cur.execute("""select p.post_id, p.title, p.content, p.published, p.user_id, 
                         count(v.post_id) as votes 
                         from posts p left join votes v 
                         on p.post_id = v.post_id 
                         where p.post_id = %s 
                         group by p.post_id""", (post_id,))
    posts = database.cur.fetchone()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with {post_id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"No data found with {book_id}"}
    database.cur.execute("""select * from users where user_id = %s""", (posts['user_id'],))
    user_data = database.cur.fetchone()
    posts['user'] = user_data
    return posts


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    database.cur.execute("""delete from posts where post_id = %s returning *""", (post_id,))
    delete_posts = database.cur.fetchone()
    # print(current_user.user_id)
    if not delete_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post is {post_id}")

    if delete_posts["user_id"] != current_user["user_id"]:
        database.conn.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action To Delete Post")
    else:
        database.conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schema.Response)
def update_post(post_id: int, post: schema.Post, current_user: schema.UserResp = Depends(oauth2.get_current_user)):
    database.cur.execute("""update posts set title = %s, content = %s, published = %s where post_id = %s returning *""",
                         (post.title, post.content, post.published, post_id))
    updated_post = database.cur.fetchone()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no book id {post_id}")

    if updated_post["user_id"] != current_user["user_id"]:
        database.conn.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized Action To Update Post")
    else:
        database.conn.commit()
        
    return updated_post
