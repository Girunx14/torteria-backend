# app/services/product_service.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import os

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services import category_service


def get_all(
    db: Session,
    category_id: int = None,
    only_available: bool = True,
) -> list[Product]:
    query = db.query(Product).options(joinedload(Product.category))

    if only_available:
        query = query.filter(Product.is_available == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    return query.order_by(Product.name).all()


def get_by_id(db: Session, product_id: int) -> Product:
    product = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {product_id} no encontrado",
        )
    return product


def create(db: Session, data: ProductCreate) -> Product:
    # Verificar que la categoría existe
    category_service.get_by_id(db, data.category_id)

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        category_id=data.category_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product_id: int, data: ProductUpdate) -> Product:
    product = get_by_id(db, product_id)

    # Si cambia la categoría, verificar que existe
    if data.category_id:
        category_service.get_by_id(db, data.category_id)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def update_image(db: Session, product_id: int, image_url: str) -> Product:
    product = get_by_id(db, product_id)

    # Eliminar imagen anterior si existe
    if product.image_url:
        old_path = product.image_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    product.image_url = image_url
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product_id: int) -> dict:
    product = get_by_id(db, product_id)

    # Eliminar imagen del disco si existe
    if product.image_url:
        old_path = product.image_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    db.delete(product)
    db.commit()
    return {"message": f"Producto '{product.name}' eliminado correctamente"}