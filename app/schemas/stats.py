# app/schemas/stats.py
from pydantic import BaseModel, field_serializer
from typing import List
from decimal import Decimal


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    total_sold: int
    total_revenue: float


class DailySales(BaseModel):
    date: str
    total_orders: int
    total_revenue: float


class StatsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    average_ticket: float
    top_products: List[TopProduct]
    daily_sales: List[DailySales]