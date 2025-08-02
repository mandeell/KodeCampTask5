# file_handler.py
import json
from pathlib import Path
from fastapi import HTTPException
from typing import Dict, Any

DATA_FILE = Path('applications.json')

def read_applications() -> Dict[str, Any]:
    """
    Read job applications from JSON file.
    
    Returns:
        Dict containing all job applications
        
    Raises:
        HTTPException: If file is corrupted or cannot be read
    """
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        return {}
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Corrupted applications.json file: {str(e)}"
        )
    except PermissionError:
        raise HTTPException(
            status_code=500, 
            detail="Permission denied: Cannot read applications.json file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to read applications data: {str(e)}"
        )

def write_applications(applications: Dict[str, Any]) -> None:
    """
    Write job applications to JSON file.
    
    Args:
        applications: Dictionary of job applications to save
        
    Raises:
        HTTPException: If file cannot be written
    """
    try:
        # Ensure the directory exists
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(applications, f, indent=2, ensure_ascii=False)
    except PermissionError:
        raise HTTPException(
            status_code=500, 
            detail="Permission denied: Cannot write to applications.json file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to write applications data: {str(e)}"
        )

def backup_applications() -> None:
    """
    Create a backup of the current applications file.
    
    Raises:
        HTTPException: If backup cannot be created
    """
    try:
        if DATA_FILE.exists():
            backup_file = DATA_FILE.with_suffix('.backup.json')
            with open(DATA_FILE, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create backup: {str(e)}"
        )