# file_handler.py
import os
from pathlib import Path
from fastapi import HTTPException
from typing import Dict, Any
import datetime

NOTES_DIR = Path('notes')

def ensure_notes_dir():
    """
    Ensure the notes directory exists.
    
    Raises:
        HTTPException: If directory cannot be created
    """
    try:
        os.makedirs(NOTES_DIR, exist_ok=True)
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create notes directory: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error creating notes directory: {str(e)}"
        )

def get_file_path(title: str) -> Path:
    """
    Get the file path for a note title.
    
    Args:
        title: Note title
        
    Returns:
        Path object for the note file
    """
    return NOTES_DIR / f"{title}.txt"

def save_note(title: str, content: str) -> Dict[str, Any]:
    """
    Save a note to a text file.
    
    Args:
        title: Note title (used as filename)
        content: Note content
        
    Returns:
        Dictionary with file information
        
    Raises:
        HTTPException: If note cannot be saved
    """
    try:
        ensure_notes_dir()
        file_path = get_file_path(title)
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get file stats
        stat = os.stat(file_path)
        
        return {
            "file_path": str(file_path),
            "file_size": stat.st_size,
            "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
    except PermissionError:
        raise HTTPException(
            status_code=403, 
            detail=f"Permission denied: Cannot write note '{title}'"
        )
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to save note '{title}': {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error saving note '{title}': {str(e)}"
        )

def read_note(title: str) -> Dict[str, Any]:
    """
    Read a note from a text file.
    
    Args:
        title: Note title
        
    Returns:
        Dictionary with note content and file information
        
    Raises:
        HTTPException: If note cannot be read or doesn't exist
    """
    try:
        file_path = get_file_path(title)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Note '{title}' not found"
            )
        
        # Read content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get file stats
        stat = os.stat(file_path)
        
        return {
            "content": content,
            "file_path": str(file_path),
            "file_size": stat.st_size,
            "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
    except HTTPException:
        raise
    except PermissionError:
        raise HTTPException(
            status_code=403, 
            detail=f"Permission denied: Cannot read note '{title}'"
        )
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to read note '{title}': {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error reading note '{title}': {str(e)}"
        )

def update_note(title: str, content: str) -> Dict[str, Any]:
    """
    Update an existing note.
    
    Args:
        title: Note title
        content: New content
        
    Returns:
        Dictionary with updated file information
        
    Raises:
        HTTPException: If note doesn't exist or cannot be updated
    """
    try:
        file_path = get_file_path(title)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Note '{title}' not found"
            )
        
        # Update content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get updated file stats
        stat = os.stat(file_path)
        
        return {
            "file_path": str(file_path),
            "file_size": stat.st_size,
            "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
    except HTTPException:
        raise
    except PermissionError:
        raise HTTPException(
            status_code=403, 
            detail=f"Permission denied: Cannot update note '{title}'"
        )
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update note '{title}': {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error updating note '{title}': {str(e)}"
        )

def delete_note(title: str) -> Dict[str, str]:
    """
    Delete a note file.
    
    Args:
        title: Note title
        
    Returns:
        Dictionary with deletion confirmation
        
    Raises:
        HTTPException: If note doesn't exist or cannot be deleted
    """
    try:
        file_path = get_file_path(title)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Note '{title}' not found"
            )
        
        # Delete file
        os.remove(file_path)
        
        return {
            "message": f"Note '{title}' deleted successfully",
            "deleted_file": str(file_path)
        }
        
    except HTTPException:
        raise
    except PermissionError:
        raise HTTPException(
            status_code=403, 
            detail=f"Permission denied: Cannot delete note '{title}'"
        )
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete note '{title}': {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error deleting note '{title}': {str(e)}"
        )

def list_notes() -> Dict[str, Any]:
    """
    List all available notes.
    
    Returns:
        Dictionary with list of notes and metadata
        
    Raises:
        HTTPException: If notes cannot be listed
    """
    try:
        ensure_notes_dir()
        
        notes = []
        for file_path in NOTES_DIR.glob('*.txt'):
            try:
                stat = os.stat(file_path)
                notes.append({
                    "title": file_path.stem,
                    "file_size": stat.st_size,
                    "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except OSError:
                # Skip files that can't be accessed
                continue
        
        return {
            "notes": notes,
            "total_count": len(notes),
            "notes_directory": str(NOTES_DIR)
        }
        
    except OSError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to list notes: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error listing notes: {str(e)}"
        )

def note_exists(title: str) -> bool:
    """
    Check if a note exists.
    
    Args:
        title: Note title
        
    Returns:
        True if note exists, False otherwise
    """
    try:
        file_path = get_file_path(title)
        return os.path.exists(file_path)
    except Exception:
        return False