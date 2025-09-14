from fastapi import APIRouter, HTTPException, Response, Depends, status
from .. import model, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_session
from typing import Annotated
from sqlmodel import Session, select

router = APIRouter(tags=["Authentication"])
SessionDep = Annotated[Session, Depends(get_session)]
# pas = OAuth2PasswordRequestForm = Depends()

@router.post('/login', response_model= schemas.Token)
def login(db: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    user = db.exec(select(model.User).filter(model.User.email == user_credentials.username)).first()
    # print("user--> ",user)

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid Credential")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid Credential")

    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}