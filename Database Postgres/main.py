from fastapi import FastAPI,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, session
import models
from database import engine,SessionLocal
from typing import Annotated,Optional
from models import Posts
from pydantic_schemas import CreatePost, UpdatePost
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
def get_posts_all(db:db_dependency):
    return db.query(Posts).all()

@app.get('/getpost/{post_id}')
def get_post_specific(db:db_dependency,post_id:int):
    return db.query(Posts).filter(Posts.id==post_id).first()

@app.post("/createpost")
def create_post(db:db_dependency,user_post:CreatePost):
    
    new_user_post=Posts(**user_post.model_dump(),created_at=datetime.now(timezone.utc))
    db.add(new_user_post)
    db.commit()
    return HTTPException(status_code=201,detail="Post created.")

@app.put('/update/{post_id}')
def update_post(db:db_dependency,post_id:int,updated_post:UpdatePost):
    user_post=db.query(Posts).filter(Posts.id==post_id).first()
    if user_post is  None:
        raise HTTPException(status_code=404,detail="Post not found.")
    updated_post_data=updated_post.model_dump(exclude_unset=True)

    for key,value in updated_post_data.items():
        # user_post.key=value
        setattr(user_post,key,value)
    
    db.commit()
    return JSONResponse(status_code=200,content={'message':'Todo updated successfully.'})

@app.delete('/delete/{post_id}')
def delete_post(db:db_dependency,post_id:int):
    user_post=db.query(Posts).filter(Posts.id==post_id).first()
    if user_post is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    db.query(Posts).filter(Posts.id==post_id).delete()
    db.commit()

    return JSONResponse(status_code=200,content={'message':'Post deleted successfully.'}) 
