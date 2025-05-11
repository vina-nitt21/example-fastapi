from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "hello"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXP_MINS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXP_MINS)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, creds_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise creds_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise creds_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "cant validate creds", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, creds_exception)

# you can use this function to fetch the user as well and not just call verify tokeen function


# alembic - makes changes to database - ie, update schema and it reflects directly, sqlalchemy leaves a table
# untouched if a table already exists, ie. alembic- incremental changes and track them. 
# dB migration tools - GIT for DB