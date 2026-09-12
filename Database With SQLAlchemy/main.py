from fastapi import FastAPI,Depends, HTTPException
import tables
from tables import Todos
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from router import authentication,admin
from router.authentication import get_current_user


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
app.include_router(admin.router)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@app.get('/')
def read_todos(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")
    return db.query(Todos).filter(Todos.owner_id==user.get('owner_id'))

@app.get('/todos/{todo_id}')
def read_specific_todos(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")

    specific_todo=db.query(Todos).filter(Todos.owner_id==user.get('owner_id')).filter(Todos.id==todo_id).first()

    if (specific_todo):
        return specific_todo
    else:
        raise HTTPException(status_code=404,detail='Todo not found.')

@app.post('/create')
def create_todos(user:user_dependency,db:db_dependency,new_todo:Todo):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")

    todo_model=Todos(**new_todo.model_dump(),owner_id=user.get('id'))
    db.commit(todo_model)
    return JSONResponse(status_code=201,content={"message":"Todo Created Successfully"})

@app.put('/update/{todo_id}')
def update_todos(user:user_dependency,db:db_dependency,todo_id:int,update_todo:UpdateTodo):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")

    todo=db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()
    if todo is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    update_data=update_todo.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(todo,key,value)

    db.commit()

    return JSONResponse(status_code=200,content={'message':'Todo updated successfully.'})

@app.delete('/remove/{todo_id}')
def delete_todos(user:user_dependency,db:db_dependency,todo_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")

    todo=db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()
    if todo is  None:
        raise HTTPException(status_code=404,detail="Todo not found.")
    
    db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).delete()
    db.commit()

    return JSONResponse(status_code=200,content={'message':'Todo deleted successfully.'}) 