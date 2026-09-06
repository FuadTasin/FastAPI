from fastapi import FastAPI,Depends, HTTPException
import tables
from tables import Todos
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from router import authentication


app=FastAPI()

class Todo(BaseModel):
    title:Annotated[str,""]
    description:Annotated[str,""]
    priority:Annotated[int,Field(gt=0,le=5,description="")]
    completed:Annotated[bool,Field(default=False)]

class UpdateTodo(BaseModel):
    title:Optional[str]=Field(default=None)
    description:Optional[str]=Field(default=None)
    priority:Optional[int]=Field(gt=0,lt=6,default=None)
    completed:Optional[bool]=Field(default=None)

tables.Base.metadata.create_all(bind=engine)
app.include_router(authentication.router)

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

@app.post('/create')
def create_todos(db:db_dependency,new_todo:Todo):
    todo_model=Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Todo Created Successfully"})

@app.put('/update/{todo_id}')
def update_todos(db:db_dependency,todo_id:int,update_todo:UpdateTodo):
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    update_data=update_todo.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(todo,key,value)

    db.commit()

    return JSONResponse(status_code=200,content={'message':'Todo updated successfully.'})

@app.delete('/remove/{todo_id}')
def delete_todos(db:db_dependency,todo_id:int):
    todo=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()

    return JSONResponse(status_code=200,content={'message':'Todo deleted successfully.'}) 