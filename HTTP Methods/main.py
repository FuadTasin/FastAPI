from fastapi import FastAPI,Path,HTTPException
import json

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