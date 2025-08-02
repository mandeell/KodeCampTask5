from pydantic import BaseModel, field_validator
from typing import Dict

class ProductCreate(BaseModel):
    id: int
    name: str
    price: float

    @field_validator("id")
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Product ID must be positive")
        return value

    @field_validator("name")
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        return value

    @field_validator("price")
    def price_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value

class Product(ProductCreate):
    pass
