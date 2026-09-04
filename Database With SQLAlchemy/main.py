from fastapi import FastAPI,Depends, HTTPException
import tables
from tables import Todos
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal

app=FastAPI()

tables.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@app.get('/')
def read_todos(db:db_dependency):
    return db.query(Todos).all()

@app.get('/todos/{todo_id}')
def read_specific_todos(db:db_dependency,todo_id:int):
    specific_todo=db.query(Todos).filter(Todos.id==todo_id).first()

    if (specific_todo):
        return specific_todo
    else:
        raise HTTPException(status_code=404,detail='Todo not found.')