from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "Raffay",
        "age": 19,
        "University": "UCP"   
    },
    2: {
        "name": "Hannan",
        "age": 17,
        "University": "UMT"
    },
    3: {
        "name": "Rehman",
        "age": 21,
        "University": "UOL"
    }    
}

class Student(BaseModel):
    name: str
    age: int
    University: str    

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    University : Optional[str] = None 

#GET:

@app.get("/")
def hello():
    return {"message": "Hello World"}

# Path Parameters:
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="Enter the ID of the student you want to view:", ge=1)):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

# Query Parameters:
@app.get('/get-by-name')
def get_student_by_name(*,name: Optional[str] = None):
    for student in students.values():
        if student["name"].lower() == name.lower():
            return student
    raise HTTPException(status_code=404, detail="Student name not found")

#POST:

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        raise HTTPException(status_code = 404, detail = "Student already exists")
    students[student_id] = student
    return students[student_id]

# PUT:

@app.put('/update-student/{student_id}')
def Update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        raise HTTPException(status_code = 404, detail = "Student not found")
    if student.name != None:
        students[student_id]["name"] = student.name
        
    if student.age != None:
        students[student_id]["age"] = student.age
        
    if student.University != None:
        students[student_id]["University"] = student.University      
        
# DELETE:

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"Message" : "Student Successfully Deleted"}