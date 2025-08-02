# models.py
from pydantic import BaseModel, field_validator
from typing import Optional
import re

class ContactCreate(BaseModel):
    name: str
    phone: str
    email: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        # Normalize name to title case
        return value.strip().title()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if not value or not value.strip():
            raise ValueError("Phone cannot be empty")
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', value)
        
        # Check if we have a reasonable number of digits (7-15)
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError("Phone must contain 7-15 digits")
        
        # Return the original format (allow various formats)
        return value.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not value or not value.strip():
            raise ValueError("Email cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value.strip()):
            raise ValueError("Invalid email format")
        
        return value.strip().lower()

class Contact(ContactCreate):
    pass

class ContactUpdate(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value
        
        if not value.strip():
            raise ValueError("Phone cannot be empty")
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', value)
        
        # Check if we have a reasonable number of digits (7-15)
        if len(digits_only) < 7 or len(digits_only) > 15:
            raise ValueError("Phone must contain 7-15 digits")
        
        return value.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if value is None:
            return value
            
        if not value.strip():
            raise ValueError("Email cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value.strip()):
            raise ValueError("Invalid email format")
        
        return value.strip().lower()