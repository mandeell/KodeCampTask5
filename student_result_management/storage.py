import json
from logging import exception
from pathlib import Path
from fastapi import HTTPException

DATA_FILE = Path('students.json')

def read_students():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted students.json file")
    except exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to read students data: {str(e)}')

def write_students(students):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(students, f, indent=2)
    except exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to write students data: {str(e)}')