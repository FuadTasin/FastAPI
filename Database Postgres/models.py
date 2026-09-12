from pydoc import text
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,DateTime,Integer,String,Boolean, true
from datetime import datetime
from datetime import timezone

class Posts(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,default=True)
    created_at=Column(TIMESTAMP(timezone=true),nullable=False,server_default=text('now()'))