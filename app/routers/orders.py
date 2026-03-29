# app/routers/orders.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services import order_service
from app.utils.security import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Órdenes"])


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    order_status: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Obtiene todas las órdenes. Solo admin."""
    return order_service.get_all(db, order_status)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Obtiene una orden por ID. Solo admin."""
    return order_service.get_by_id(db, order_id)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una nueva orden. Público.
    No requiere autenticación para que el cliente pueda ordenar
    directamente desde el menú.
    """
    return order_service.create(db, data)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Actualiza el estado de una orden. Solo admin."""
    return order_service.update_status(db, order_id, data)


@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Elimina una orden. Solo admin."""
    return order_service.delete(db, order_id)