from warnings import deprecated
from fastapi import FastAPI,APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr, Field
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.responses import JSONResponse
from tables import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
class CreateUsers(BaseModel):
    email:EmailStr=Field(description="Email of the user")
    username:Annotated[str,"username of the user"]
    firstname:Annotated[str,"firstname of the user"]
    lastname:Annotated[str,"lastname of the user"]
    password:Annotated[str,"Password of the user"]
    role:Annotated[str,"Role of the user"]

def authenticate_user(username,password,db):
    user=db.query(Users).filter(Users.username==username).first()
    if user is  None:
        return False
    if bcrypt_context.verify(password,user.hash_password):
        return True
    return False

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@router.post('/createuser')
def create_user(db:db_dependency,new_user:CreateUsers):
    user_model=Users(
        email=new_user.email,
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        hash_password=bcrypt_context.hash(new_user.password),
        is_active=True,
        role=new_user.role
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201,content={'message':'User created successfully.'})

@router.post('/login')
def login_user(db:db_dependency,form_user:Annotated[OAuth2PasswordRequestForm,Depends()]):
    
    user=authenticate_user(form_user.username,form_user.password,db)
    
    if user==True:
        return "Authenticated user."
    else:
        return "Failed Authentication."
