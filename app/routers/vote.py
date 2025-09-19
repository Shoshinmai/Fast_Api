from fastapi import status, HTTPException, APIRouter, Depends
from .. import model, schemas, database, oauth2
from typing import Annotated
from sqlmodel import Session, select

router = APIRouter(
    prefix= "/vote",
    tags= ["Vote"]
)
SessionDep = Annotated[Session, Depends(database.get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:SessionDep, current_user: int= Depends(oauth2.get_current_user)):
    
    post = db.exec(select(model.Post).filter(model.Post.id == vote.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with the id: {vote.post_id} does not exist.")
    
    vote_query = db.exec(select(model.Vote).filter(model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id))
    found_user = vote_query.first()
    
    if vote.dir == 1:
        if found_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added the vote"}
    else:
        if not found_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        db.delete(found_user)
        db.commit()
        
        return {"message": "Successfully delted the post"}