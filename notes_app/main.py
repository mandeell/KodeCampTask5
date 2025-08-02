# main.py (initial)
from fastapi import FastAPI, HTTPException
from models import NoteCreate, Note
from file_handler import save_note

app = FastAPI()

@app.post("/notes", status_code=201)
async def create_note(note: NoteCreate):
    try:
        save_note(note.title, note.content)
        return Note(**note.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")