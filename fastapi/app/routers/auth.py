from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schema, utils, database, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schema.Token)
# def login(user_credentials: schema.UserLogin):
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    database.cur.execute("""select * from users where email= %s""",
                         (user_credentials.username,))
    user = database.cur.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
 
    if not utils.hash_verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user["user_id"]})
    # return a token
    return {"access_token": access_token, "token_type": "bearer"}
