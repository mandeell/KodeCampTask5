# models.py
from pydantic import BaseModel, field_validator
from typing import Optional
import re

class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator('title')
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        # Sanitize title: remove invalid characters, limit length
        sanitized = re.sub(r'[^\w\-]', '_', value.strip())[:100]
        if not sanitized:
            raise ValueError("Title contains only invalid characters")
        return sanitized

    @field_validator('content')
    def validate_content(cls, value):
        if not value.strip():
            raise ValueError("Content cannot be empty")
        return value

class Note(NoteCreate):
    pass