from fastapi import FastAPI, HTTPException
from models import Student
from storage import read_students, write_students

app = FastAPI(title="Student Result Management System")

@app.post("/students/")
async def create_student(student: Student):
    try:
        students = read_students()
        if student.name in students:
            raise HTTPException(status_code=400, detail='Student already exists')
        
        # Store the student data
        students[student.name] = student.model_dump()
        write_students(students)
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to create student: {str(e)}')

@app.get("/students/{name}")
async def get_student(name: str):
    try:
        # Convert name to title case for consistent lookup
        name_title = name.strip().title()
        students = read_students()
        if name_title not in students:
            raise HTTPException(status_code=404, detail='Student not found')
        return Student(**students[name_title])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to retrieve student: {str(e)}')

@app.get("/students/")
async def get_all_students():
    try:
        students = read_students()
        return [Student(**data) for data in students.values()]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to retrieve students: {str(e)}')