from time import timezone
from warnings import deprecated
from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr, Field
from typing import Annotated
from pydantic.types import _secret_display
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.responses import JSONResponse
from tables import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta,datetime,timezone
from router.authentication import get_current_user
from tables import Todos

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get('/admin/todo')
def read_all_todos(user:user_dependency,db:db_dependency):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail="Failed Authentication")

    return db.query(Todos).all()

@router.delete('/admin/remove/{todo_id}')
def delete_todos_by_admin(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None or user.get('role')=='admin':
        raise HTTPException(status_code=401,detail="Failed Authentication")

    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()

    return JSONResponse(status_code=200,content={'message':'Todo deleted successfully.'}) 


    