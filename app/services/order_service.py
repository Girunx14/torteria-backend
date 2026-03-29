# app/services/order_service.py
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from decimal import Decimal

from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate
from app.services import product_service


def get_all(db: Session, status: str = None) -> list[Order]:
    query = db.query(Order).options(joinedload(Order.items))

    if status:
        query = query.filter(Order.status == status)

    return query.order_by(Order.created_at.desc()).all()


def get_by_id(db: Session, order_id: int) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con id {order_id} no encontrada",
        )
    return order


def create(db: Session, data: OrderCreate, user_id: int = None) -> Order:
    total = Decimal("0.00")
    order_items = []

    # Verificar productos y calcular total
    for item_data in data.items:
        product = product_service.get_by_id(db, item_data.product_id)

        if not product.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto '{product.name}' no está disponible",
            )

        unit_price = Decimal(str(product.price))
        total += unit_price * item_data.quantity

        order_items.append(OrderItem(
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=unit_price,
        ))

    # Crear la orden
    order = Order(
        user_id=user_id,
        total=total,
        notes=data.notes,
        items=order_items,
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_status(db: Session, order_id: int, data: OrderUpdate) -> Order:
    order = get_by_id(db, order_id)

    if data.status:
        try:
            order.status = OrderStatus(data.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Opciones: pending, completed, cancelled",
            )

    if data.notes is not None:
        order.notes = data.notes

    db.commit()
    db.refresh(order)
    return order


def delete(db: Session, order_id: int) -> dict:
    order = get_by_id(db, order_id)
    db.delete(order)
    db.commit()
    return {"message": f"Orden #{order_id} eliminada correctamente"}