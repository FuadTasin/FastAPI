from ctypes import alignment
from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic_schemas import CreateUser
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt
from datetime import timedelta,datetime,timezone

router=APIRouter()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
OAuth2_bearer=OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY="127cf0676824de422291e1ea30ef45abb1015d7dec46ca7cc3eba952e830e337"
ALGORITHM="HS256"

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
        return user
    return False

def create_user_token(username:str,user_id:int,expires_delta:timedelta):
    encode={'sub':username,'id':user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:Annotated[str,Depends(OAuth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:str=payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=404,detail="User not found")
        return {'username':username,'id':user_id}
    except:
        raise HTTPException(status_code=404,detail="User not found")


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
    if not user:
        return "Failed Authentication"
    token=create_user_token(user.username,user.id,timedelta(minutes=30))
    return token