# app/routers/categories.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service
from app.utils.security import require_admin

router = APIRouter(prefix="/categories", tags=["Categorías"])


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
):
    """Obtiene todas las categorías. Público."""
    return category_service.get_all(db, include_inactive)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene una categoría por ID. Público."""
    return category_service.get_by_id(db, category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Crea una nueva categoría. Solo admin."""
    return category_service.create(db, data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Actualiza una categoría. Solo admin."""
    return category_service.update(db, category_id, data)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Elimina una categoría. Solo admin."""
    return category_service.delete(db, category_id)