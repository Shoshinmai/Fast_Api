from fastapi import  Response, status, HTTPException, APIRouter, Depends
from sqlmodel import select,func
from .. import model, schemas,oauth2
from ..database import get_session
from typing import Annotated, Optional
from sqlmodel import Session

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)
SessionDep = Annotated[Session, Depends(get_session)] 

@router.get("/", response_model = list[schemas.PostOut])
# @router.get("/")
def get_posts(db: SessionDep, current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # post = cursor.fetchall()
    # posts = db.exec(select(model.Post).filter(model.Post.ownerid == current_user.id)).all() //this line of code is to get only post which are under user authorization
    # posts = db.exec(select(model.Post).filter(model.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip)).all()
    posts = db.exec(select(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Post.id == model.Vote.post_id, isouter=True).
                     group_by(model.Post.id).filter(model.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip)).all()
    # return [{"post": post, "votes": votes} for post, votes in result]
    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = model.Post(title=post.title, content=post.content, published=post.published)
    print(current_user)
    new_post = model.Post(ownerid=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.PostOut)
def get_posts(id : int, db: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.exec(select(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Post.id == model.Vote.post_id, isouter=True).
                     group_by(model.Post.id).filter(model.Post.id == id)).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details of the post id: {id} is not found.")
    # if post.ownerid != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorize to perform requested action.")
    return post
    

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s Returning *""", (str(id)))
    # del_post = cursor.fetchone()
    # conn.commit()
    post = db.get(model.Post, id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details of the post id: {id} is not found.")
    if post.ownerid != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize to perform requested action.")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # up_post = cursor.fetchone()
    # conn.commit()
    existing_post = db.get(model.Post, id)
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details of the post id: {id} is not found.")
    if existing_post.ownerid != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorize to perform requested action.")
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    db.add(existing_post)
    db.commit()
    db.refresh(existing_post)
    return existing_post