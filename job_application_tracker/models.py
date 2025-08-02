# models.py
from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INTERVIEW = "interview"
    WITHDRAWN = "withdrawn"

class JobApplicationCreate(BaseModel):
    name: str
    company: str
    position: str
    status: Status = Status.PENDING

    @field_validator('name', 'company', 'position')
    @classmethod
    def must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Field cannot be empty")
        return value.strip().title()

class JobApplication(JobApplicationCreate):
    id: str  # Generated as name_company_position

    @field_validator('id')
    @classmethod
    def id_must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("ID cannot be empty")
        return value