# file_handler.py
import json
from pathlib import Path
from fastapi import HTTPException

DATA_FILE = Path('contacts.json')

def read_contacts():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupted contacts.json file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read contacts data: {str(e)}")

def write_contacts(contacts):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write contacts data: {str(e)}")