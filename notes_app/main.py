# main.py
from fastapi import FastAPI, HTTPException
from models import NoteCreate, Note, NoteUpdate
from file_handler import (
    save_note, read_note, update_note, delete_note, 
    list_notes, note_exists
)
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notes API",
    description="FastAPI app to add, update, and delete notes saved as text files",
    version="1.0.0"
)

@app.post("/notes/", status_code=201, response_model=Note)
async def create_note(note: NoteCreate):
    """
    Create a new note and save it as a .txt file.
    
    Args:
        note: Note data with title and content
        
    Returns:
        Created note with file information
        
    Raises:
        HTTPException: If note creation fails or note already exists
    """
    try:
        # Check if note already exists
        if note_exists(note.title):
            raise HTTPException(
                status_code=409, 
                detail=f"Note '{note.title}' already exists. Use PUT to update."
            )
        
        # Save note and get file info
        file_info = save_note(note.title, note.content)
        
        # Create response
        response_note = Note(
            title=note.title,
            content=note.content,
            **file_info
        )
        
        logger.info(f"Created note: {note.title}")
        return response_note
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating note '{note.title}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create note: {str(e)}"
        )

@app.get("/notes/{title}", response_model=Note)
async def get_note(title: str):
    """
    Get a note by title from its .txt file.
    
    Args:
        title: Note title
        
    Returns:
        Note with content and file information
        
    Raises:
        HTTPException: If note doesn't exist or cannot be read
    """
    try:
        # Read note and get file info
        note_data = read_note(title)
        
        # Create response
        response_note = Note(
            title=title,
            content=note_data["content"],
            file_path=note_data["file_path"],
            file_size=note_data["file_size"],
            created_at=note_data["created_at"],
            modified_at=note_data["modified_at"]
        )
        
        logger.info(f"Retrieved note: {title}")
        return response_note
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving note '{title}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve note: {str(e)}"
        )

@app.post("/notes/{title}", response_model=Note)
async def update_note_post(title: str, note_update: NoteUpdate):
    """
    Update an existing note using POST method.
    
    Args:
        title: Note title
        note_update: New content for the note
        
    Returns:
        Updated note with file information
        
    Raises:
        HTTPException: If note doesn't exist or cannot be updated
    """
    try:
        # Update note and get file info
        file_info = update_note(title, note_update.content)
        
        # Create response
        response_note = Note(
            title=title,
            content=note_update.content,
            **file_info
        )
        
        logger.info(f"Updated note: {title}")
        return response_note
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating note '{title}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update note: {str(e)}"
        )

@app.delete("/notes/{title}")
async def delete_note_endpoint(title: str):
    """
    Delete a note by removing its .txt file.
    
    Args:
        title: Note title
        
    Returns:
        Deletion confirmation message
        
    Raises:
        HTTPException: If note doesn't exist or cannot be deleted
    """
    try:
        # Delete note
        result = delete_note(title)
        
        logger.info(f"Deleted note: {title}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting note '{title}': {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete note: {str(e)}"
        )

@app.get("/notes/")
async def list_all_notes():
    """
    List all available notes.
    
    Returns:
        Dictionary with list of notes and metadata
        
    Raises:
        HTTPException: If notes cannot be listed
    """
    try:
        result = list_notes()
        logger.info(f"Listed {result['total_count']} notes")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing notes: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to list notes: {str(e)}"
        )

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information and usage instructions
    """
    return {
        "message": "Notes API - FastAPI app to manage notes as text files",
        "endpoints": {
            "POST /notes/": "Create a new note",
            "GET /notes/{title}": "Get a note by title",
            "POST /notes/{title}": "Update a note",
            "DELETE /notes/{title}": "Delete a note",
            "GET /notes/": "List all notes"
        },
        "features": [
            "Save each note as a .txt file",
            "Use os module for file operations",
            "Comprehensive error handling",
            "File metadata tracking"
        ]
    }