from fastapi import status, APIRouter, HTTPException
from .. import schema, utils, database as db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate):
    # hash the password
    user.password = utils.hash_pwd(user.password)
    query = """insert into users (email, password) values (%s, %s) returning *"""
    params = (user.email, user.password)
    user = db.execute_sql_query(query, *params)
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Invalid user name")
    return user


@router.get("/{user_id}", response_model=schema.UserResp)
def get_user(user_id: int):
    query = """select * from users where user_id= %s"""
    params = (str(user_id))
    user = db.execute_sql_query(query, params)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with {user_id}")
    return user[0]
