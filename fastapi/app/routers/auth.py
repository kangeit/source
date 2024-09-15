from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schema, utils, oauth2, database

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schema.Token)
# def login(user_credentials: schema.UserLogin):
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    query = """select * from users where email= %s"""
    params = (user_credentials.username,)
    user = database.execute_sql_query(query, *params)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
 
    if not utils.hash_verify(user_credentials.password, user[0]["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user[0]["user_id"]})
    # return a token
    return {"access_token": access_token, "token_type": "bearer"}
