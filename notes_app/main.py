# main.py
from fastapi import FastAPI, HTTPException
from models import NoteCreate, Note
from file_handler import save_note, read_note, delete_note

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

@app.get("/notes/{title}")
async def get_note(title: str):
    try:
        content = read_note(title)
        return Note(title=title, content=content)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve note: {str(e)}")

@app.put("/notes/{title}")
async def update_note(title: str, note: NoteCreate):
    if title != note.title:
        raise HTTPException(status_code=400, detail="Title in URL must match note title")
    try:
        save_note(note.title, note.content)
        return Note(**note.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update note: {str(e)}")

@app.delete("/notes/{title}")
async def delete_note_endpoint(title: str):
    try:
        delete_note(title)
        return {"detail": f"Note {title} deleted"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete note: {str(e)}")