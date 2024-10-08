from fastapi import Depends, status, HTTPException, APIRouter
from .. import schema, database, oauth2
from psycopg.errors import ForeignKeyViolation

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_vote(vote: schema.Vote, current_user: schema.UserResp = Depends(oauth2.get_current_user)):

    query = """select * from votes where post_id = %s and user_id=%s"""
    params = (vote.post_id, current_user["user_id"])
    voted_post = database.execute_sql_query(query, *params)
 
    if vote.dir == 1:
        if voted_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user['user_id']} has already voted on post {vote.post_id}")
        try:
            database.execute_sql_query("""insert into votes (post_id, user_id) values (%s, %s) returning *""",
                                 *(vote.post_id, current_user["user_id"]))
        except ForeignKeyViolation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Post {vote.post_id} does not exists")
        return {"message": "successfully voted"}
    else:
        if not voted_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")

        database.execute_sql_query("""delete from votes where post_id = %s and user_id = %s returning *""",
                             *(vote.post_id, current_user["user_id"]))
        return {"message": "successfully delete vote"}
