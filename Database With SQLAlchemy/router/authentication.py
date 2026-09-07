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

router=APIRouter()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
OAuth2_bearer=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="26f95f43e1f116ec14d4be9c839dc0a3e8c93ca75e696a0af661fa46b0c186c4"
ALGORITHM="HS256"
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
        return user
    return False

def create_access_token(user_name:str,user_id:int,expire_delta:timedelta):
    encode={
        'sub':user_name,
        'id':user_id,
    }
    expire=datetime.now(timezone.utc)+expire_delta
    encode.update({
        'exp':expire
    })

    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:Annotated[str,Depends(OAuth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=404,detail="User not found.")
        return {
            'username':username,
            'id':id
        }
    except:
        raise JWTError

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
    
    if not user:
        return "Failed Authentication."
    token=create_access_token(user.username,user.id,timedelta(minutes=30))
    return {
        'access_token':token,
        'token_type':'bearer'
    }