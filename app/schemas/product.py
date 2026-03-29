# app/schemas/product.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, examples=["Torta de Milanesa"])
    description: Optional[str] = Field(None, examples=["Milanesa con aguacate y jitomate"])
    price: Decimal = Field(..., gt=0, decimal_places=2, examples=[65.00])
    category_id: int = Field(..., gt=0)

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category_id: Optional[int] = Field(None, gt=0)
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    image_url: Optional[str] = None
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductWithCategory(ProductResponse):
    category: Optional[object] = None

    model_config = {"from_attributes": True}