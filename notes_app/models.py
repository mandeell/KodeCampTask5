# models.py
from pydantic import BaseModel, field_validator
from typing import Optional
import re
import os

class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator('title')
    @classmethod
    def validate_title(cls, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        
        # Sanitize title: remove invalid filename characters
        # Keep alphanumeric, spaces, hyphens, underscores
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', value.strip())
        sanitized = sanitized[:100]  # Limit length for filesystem compatibility
        
        if not sanitized:
            raise ValueError("Title contains only invalid characters")
        return sanitized

    @field_validator('content')
    @classmethod
    def validate_content(cls, value):
        if value is None:
            raise ValueError("Content cannot be None")
        # Allow empty content for notes
        return value

class Note(NoteCreate):
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None

class NoteUpdate(BaseModel):
    content: str

    @field_validator('content')
    @classmethod
    def validate_content(cls, value):
        if value is None:
            raise ValueError("Content cannot be None")
        return value