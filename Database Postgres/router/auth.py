from email import message
from typing import Annotated
from warnings import deprecated
from fastapi import FastAPI,APIRouter,Depends
import fastapi
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic_schemas import CreateUser
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

def authenticate_user(username,password,db):
    user=db.query(Users).filter(Users.username==username).first()
    if user is None:
        return False
    if bcrypt_context.verify(password,user.hash_password):
        return True
    return False

@router.post('/create/users')
def create_users(db:db_dependency,new_user:CreateUser):
    new_user_data=Users(
        email=new_user.email,
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        hash_password=bcrypt_context.hash(new_user.password),
        is_active=True,
        role=new_user.role
    )
    db.add(new_user_data)
    db.commit()
    return JSONResponse(status_code=201,content={'message':'User created successfully.'})

@router.post('/login/users')
def login_users(db:db_dependency,user_form:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticate_user(user_form.username,user_form.password,db)
    if user:
        return "User Authenticated."
    else:
        return "Failed Authentication."