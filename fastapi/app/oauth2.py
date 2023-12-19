from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
# tokenURL is the endpoint of login api defined name
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = schema.TokenData(id=user_id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentials",
                                         headers={"WW-Authenticate": "Bearer"})
    user = verify_access_token(token, credential_exception)
    data = database.execute_sql_query("""select * from users where user_id= %s""",
                         *(user.id,))
    return data[0]
