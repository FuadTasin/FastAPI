from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session, session
import models
from database import engine,SessionLocal
from typing import Annotated,Optional
from models import Posts
from pydantic_schemas import CreatePost
from datetime import datetime,timezone

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@app.get("/getposts")
def get_posts(db:db_dependency):
    return db.query(Posts).all()

@app.post("/createpost")
def create_post(db:db_dependency,user_post:CreatePost):
    
    new_user_post=Posts(**user_post.model_dump())
    db.add(new_user_post)
    db.commit()
    return HTTPException(status_code=201,detail="Post created.")


