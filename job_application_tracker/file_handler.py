# file_handler.py
import json
from pathlib import Path
from fastapi import HTTPException

DATA_FILE = Path('applications.json')

def read_applications():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted applications.json file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read applications data: {str(e)}")

def write_applications(applications):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(applications, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write applications data: {str(e)}")