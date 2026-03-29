# app/utils/image_handler.py
import os
import uuid
from PIL import Image
from fastapi import HTTPException, status, UploadFile
from app.config import get_settings

settings = get_settings()

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_SIZE_BYTES = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
MAX_WIDTH = 800


def validate_and_save(file: UploadFile) -> str:
    """Valida, optimiza y guarda una imagen. Retorna la URL relativa."""

    # Validar tipo
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Usa JPG, PNG o WEBP",
        )

    # Validar tamaño
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen no debe superar {settings.MAX_IMAGE_SIZE_MB}MB",
        )

    # Generar nombre único
    extension = file.filename.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        extension = "jpg"

    filename = f"{uuid.uuid4().hex}.{extension}"
    filepath = os.path.join(settings.UPLOAD_FOLDER, filename)

    # Procesar y guardar con Pillow
    with Image.open(file.file) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

        img.save(filepath, optimize=True, quality=85)

    return f"/uploads/{filename}"


def delete_image(image_url: str) -> None:
    """Elimina una imagen del disco si existe."""
    if not image_url:
        return
    filepath = image_url.lstrip("/")
    if os.path.exists(filepath):
        os.remove(filepath)