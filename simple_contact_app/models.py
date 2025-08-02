# models.py
from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
import re

class ContactCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value.strip()

    @field_validator('phone')
    def validate_phone(cls, value):
        # Basic phone validation: + followed by 10-15 digits
        if not re.match(r'^\+\d{10,15}$', value):
            raise ValueError("Phone must be in format +1234567890 (10-15 digits)")
        return value

class Contact(ContactCreate):
    id: str