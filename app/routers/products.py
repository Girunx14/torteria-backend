# app/routers/products.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from PIL import Image
import shutil

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service
from app.utils.security import require_admin
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("/", response_model=list[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    only_available: bool = True,
    db: Session = Depends(get_db),
):
    """Obtiene todos los productos. Público."""
    return product_service.get_all(db, category_id, only_available)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene un producto por ID. Público."""
    return product_service.get_by_id(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Crea un nuevo producto. Solo admin."""
    return product_service.create(db, data)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Actualiza un producto. Solo admin."""
    return product_service.update(db, product_id, data)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Elimina un producto. Solo admin."""
    return product_service.delete(db, product_id)


# app/routers/products.py — reemplaza el endpoint upload_image
@router.post("/{product_id}/image", response_model=ProductResponse)
def upload_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """Sube o reemplaza la imagen de un producto. Solo admin."""
    from app.utils.image_handler import validate_and_save
    image_url = validate_and_save(file)
    return product_service.update_image(db, product_id, image_url)

    # Validar tamaño (5MB máximo)
    max_size = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen no debe superar {settings.MAX_IMAGE_SIZE_MB}MB",
        )

    # Generar nombre único para el archivo
    extension = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4().hex}.{extension}"
    filepath = os.path.join(settings.UPLOAD_FOLDER, filename)

    # Guardar y optimizar imagen con Pillow
    with Image.open(file.file) as img:
        # Convertir a RGB si es necesario (PNG con transparencia, etc.)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Redimensionar si es muy grande (máximo 800px de ancho)
        if img.width > 800:
            ratio = 800 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((800, new_height), Image.LANCZOS)

        img.save(filepath, optimize=True, quality=85)

    # Guardar URL en la base de datos
    image_url = f"/uploads/{filename}"
    return product_service.update_image(db, product_id, image_url)