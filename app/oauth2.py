from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from . import schemas, database, model
from sqlmodel import Session, select
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
SessionDep = Annotated[Session, Depends(database.get_session)]


SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(db: SessionDep, token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.exec(select(model.User).filter(model.User.id == token.id)).first()
    
    return user