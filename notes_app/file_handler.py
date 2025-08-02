# file_handler.py
import os
from pathlib import Path
from fastapi import HTTPException

NOTES_DIR = Path('notes')

def ensure_notes_dir():
    try:
        os.makedirs(NOTES_DIR, exist_ok=True)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notes directory: {str(e)}")

def save_note(title: str, content: str):
    ensure_notes_dir()
    file_path = NOTES_DIR / f"{title}.txt"
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to save note {title}: {str(e)}")

def read_note(title: str) -> str:
    file_path = NOTES_DIR / f"{title}.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Note {title} not found")
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to read note {title}: {str(e)}")

def delete_note(title: str):
    file_path = NOTES_DIR / f"{title}.txt"
    try:
        os.remove(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Note {title} not found")
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete note {title}: {str(e)}")

def list_notes() -> list[str]:
    ensure_notes_dir()
    try:
        return [f.stem for f in NOTES_DIR.glob('*.txt')]
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list notes: {str(e)}")