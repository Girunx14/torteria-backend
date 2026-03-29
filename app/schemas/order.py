# app/schemas/order.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1)
    notes: Optional[str] = Field(None, max_length=500)


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, examples=["completed"])
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    user_id: Optional[int]
    status: str
    total: Decimal
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}