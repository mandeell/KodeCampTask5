from fastapi import FastAPI, HTTPException
from models import Student
from storage import read_students, write_students

app = FastAPI()

@app.post("/students")
async def create_students(student: Student):
    students = read_students()
    if student.name in students:
        raise HTTPException(status_code=400, detail='Student already exists')
    students[student.name] = student.dict()
    write_students(students)
    return student

@app.get("/students/{name}")
async def get_student(name: str):
    students = read_students()
    if name not in students:
        raise HTTPException(status_code=400, detail='Student not found')
    return Student(**students[name])

@app.get("/students")
async def get_all_students():
    students = read_students()
    return [Student(**data) for data in students.values()]