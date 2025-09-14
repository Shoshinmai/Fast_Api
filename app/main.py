from fastapi import FastAPI, Depends
from typing import Annotated
from .database import init_db, get_session
from sqlmodel import Session
from .routers import post, user,auth
from .config import setting



init_db()
# SQLModel.metadata.create_all(engine)
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()
# my_posts = [{"title" : "Title of the 1st post.", "content": "Content of the post 1", "id": 1}, {"title": "Next type", "content": "Its my type", "id": 2}]
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api"}

# @app.get("/sql")
# def test(db: SessionDep):
#     posts = db.exec(select(model.Post)).all()
#     return {"data": posts}



