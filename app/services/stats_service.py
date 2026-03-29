# app/services/stats_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from decimal import Decimal

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.stats import StatsResponse, TopProduct, DailySales


def get_stats(db: Session, days: int = 30) -> StatsResponse:

    # --- Total revenue y total orders ---
    result = (
        db.query(
            func.coalesce(func.sum(Order.total), 0).label("total_revenue"),
            func.count(Order.id).label("total_orders"),
        )
        .filter(Order.status == OrderStatus.completed)
        .first()
    )

    total_revenue = Decimal(str(result.total_revenue))
    total_orders = result.total_orders
    average_ticket = (
        total_revenue / total_orders if total_orders > 0 else Decimal("0.00")
    )

    # --- Productos más vendidos ---
    top_raw = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("total_revenue"),
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status == OrderStatus.completed)
        .group_by(Product.id, Product.name)
        .order_by(desc("total_sold"))
        .limit(10)
        .all()
    )

    top_products = [
        TopProduct(
            product_id=row.product_id,
            product_name=row.product_name,
            total_sold=row.total_sold,
            total_revenue=Decimal(str(row.total_revenue)),
        )
        for row in top_raw
    ]

    # --- Ventas por día (últimos N días) ---
    daily_raw = (
        db.query(
            func.date(Order.created_at).label("date"),
            func.count(Order.id).label("total_orders"),
            func.sum(Order.total).label("total_revenue"),
        )
        .filter(Order.status == OrderStatus.completed)
        .filter(
            Order.created_at >= func.date_sub(func.now(), func.interval(days, "DAY"))
        )
        .group_by(func.date(Order.created_at))
        .order_by("date")
        .all()
    )

    daily_sales = [
        DailySales(
            date=str(row.date),
            total_orders=row.total_orders,
            total_revenue=Decimal(str(row.total_revenue)),
        )
        for row in daily_raw
    ]

    return StatsResponse(
        total_revenue=total_revenue,
        total_orders=total_orders,
        average_ticket=round(average_ticket, 2),
        top_products=top_products,
        daily_sales=daily_sales,
    )