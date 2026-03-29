# app/services/category_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_all(db: Session, include_inactive: bool = False) -> list[Category]:
    query = db.query(Category)
    if not include_inactive:
        query = query.filter(Category.is_active == True)
    return query.order_by(Category.name).all()


def get_by_id(db: Session, category_id: int) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {category_id} no encontrada",
        )
    return category


def create(db: Session, data: CategoryCreate) -> Category:
    category = Category(
        name=data.name,
        description=data.description,
    )
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{data.name}'",
        )


def update(db: Session, category_id: int, data: CategoryUpdate) -> Category:
    category = get_by_id(db, category_id)

    # Solo actualiza los campos que se enviaron
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con ese nombre",
        )


def delete(db: Session, category_id: int) -> dict:
    category = get_by_id(db, category_id)

    # Verificar si tiene productos asociados
    if category.products:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar una categoría que tiene productos asociados",
        )

    db.delete(category)
    db.commit()
    return {"message": f"Categoría '{category.name}' eliminada correctamente"}