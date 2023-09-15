from fastapi import status, APIRouter, HTTPException
from .. import schema, utils, database


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate):
    # hash the password
    user.password = utils.hash_pwd(user.password)
    database.cur.execute("""insert into users (email, password) 
    values (%s, %s) returning *""", (user.email, user.password))
    user = database.cur.fetchone()
    database.conn.commit()
    return user


@router.get("/{user_id}", response_model=schema.UserResp)
def get_user(user_id: int):
    database.cur.execute("""select * from users where user_id= %s""", (user_id,))
    user = database.cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with {user_id}")
    return user
