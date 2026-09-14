from pydoc import text

from sqlalchemy.orm import foreign
from sqlalchemy.schema import DefaultGenerator
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,DateTime, ForeignKey,Integer,String,Boolean, true
from datetime import datetime
from datetime import timezone

class Posts(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,default=True)
    created_at=Column(TIMESTAMP(timezone=true),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id"))

class Users(Base):
    __tablename__="users"

    id=Column(Integer,index=True,primary_key=True)
    email=Column(String,unique=True)
    username=Column(String,unique=True)
    firstname=Column(String)
    lastname=Column(String)
    hash_password=Column(String)
    role=Column(String)
    is_active=Column(Boolean,default=True)