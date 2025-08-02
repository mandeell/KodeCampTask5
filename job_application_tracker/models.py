# models.py
from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class JobApplicationCreate(BaseModel):
    name: str
    company: str
    position: str
    status: Status

    @field_validator('name', 'company', 'position')
    def must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value

class JobApplication(JobApplicationCreate):
    id: str  # Generated as name_company_position