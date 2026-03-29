# app/schemas/stats.py
from pydantic import BaseModel
from typing import List
from decimal import Decimal


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    total_sold: int
    total_revenue: Decimal


class DailySales(BaseModel):
    date: str
    total_orders: int
    total_revenue: Decimal


class StatsResponse(BaseModel):
    total_revenue: Decimal
    total_orders: int
    average_ticket: Decimal
    top_products: List[TopProduct]
    daily_sales: List[DailySales]