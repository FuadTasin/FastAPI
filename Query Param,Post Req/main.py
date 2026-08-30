from fastapi import FastAPI,Path,HTTPException,Query
import json

from starlette.status import HTTP_404_NOT_FOUND

app=FastAPI()

def load_data():
    with open('students.json','r') as f:
        data=json.load(f)
    return data

@app.get("/")
def hello():
    return "Student Management System App."

@app.get("/about")
def about():
    return "A fully functional API to manage our student records."

@app.get("/view")
def view_students():
    data=load_data()
    return data

@app.get("/view/{student_id}")
def view_student_by_id(student_id:str=Path(...,description="Student Id of the student",example="S001")):
    data=load_data()
    if student_id in data:
        return data[student_id]
    else:
        return HTTPException(status_code=404,detail="Student not found.")

@app.get("/sort")
def view_sorted_students(sorted_by:str=Query(...,description="Sort on the basis of class,age,roll,marks"),order:str=Query('asc',description="Choose order: asc or des")):
    
    valid_fields=['class','age','roll','Math marks','English marks','Science marks']

    if sorted_by not in valid_fields:
        return HTTPException(status_code=404,detail=f"Invalid field,select from {valid_fields}")

    if order not in ['asc','des']:
        return HTTPException(status_code=404,detail=f"Invalid order,select from {['asc','des']}")

    data=load_data()
    sort_order=True if order=='des' else False
    sorted_data=list(data.values())
    sorted_data.sort(key=lambda x:x[sorted_by],reverse=sort_order)
    return sorted_data
