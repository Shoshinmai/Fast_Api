from fastapi import status, HTTPException, APIRouter, Depends
from .. import model, schemas, utils
from ..database import get_session
from typing import Annotated
from sqlmodel import Session


router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut) 
def create_posts(user: schemas.UserCreate, db: SessionDep):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_post = model.User(**user.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: SessionDep):
    user = db.get(model.User, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details of the user id: {id} is not found.")
    return user