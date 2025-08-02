from pydantic import BaseModel, field_validator

class Product(BaseModel):
    id: int
    name: str
    price: float

    @field_validator("id")
    @classmethod
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Product ID must be positive")
        return value

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        return value.strip()

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return round(value, 2)
