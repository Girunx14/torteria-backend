# app/utils/image_handler.py
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException, status, UploadFile
from app.config import get_settings

settings = get_settings()

# Configurar Cloudinary con las variables de entorno
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_SIZE_BYTES = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024


def validate_and_save(file: UploadFile) -> str:
    """Valida, optimiza y guarda una imagen en Cloudinary. Retorna la URL segura."""

    # Validar tipo de contenido
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Usa JPG, PNG o WEBP",
        )

    # Validar tamaño del archivo
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)  # Resetear cursor al inicio para la subida

    if file_size > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen no debe superar {settings.MAX_IMAGE_SIZE_MB}MB",
        )

    # Subir imagen a Cloudinary directamente
    try:
        # Generar un string único para evitar colisiones si se desea un ID personalizado
        unique_name = uuid.uuid4().hex

        # 'upload' automáticamente carga la imagen, permite setear transformaciones
        # para emular lo que hacías con Pillow: max_width 800, quality automática
        upload_result = cloudinary.uploader.upload(
            file.file,
            folder="torteria/products",
            public_id=unique_name,
            transformation=[
                {"width": 800, "crop": "limit"},    # redimensionar si sobrepasa 800px
                {"quality": "auto", "fetch_format": "auto"} # optimización equivalente a quality=85
            ]
        )

        return upload_result.get("secure_url")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imagen a Cloudinary: {str(e)}"
        )


def delete_image(image_url: str) -> None:
    """Elimina una imagen de Cloudinary a través de su URL."""
    if not image_url or "cloudinary.com" not in image_url:
        return
        
    try:
        # Extraer el public_id de la URL.
        # Una url típica de Cloudinary es: https://res.cloudinary.com/<cloud_name>/image/upload/v1234567/torteria/products/<public_id>.jpg
        parts = image_url.split("/")
        
        # Encontramos la parte donde sigue 'torteria/products'
        if "torteria" in parts and "products" in parts:
            # Obtener el nombre del archivo sin extensión
            filename_with_ext = parts[-1]
            public_id_only = filename_with_ext.split(".")[0]
            full_public_id = f"torteria/products/{public_id_only}"
            
            cloudinary.uploader.destroy(full_public_id)
    except Exception as e:
        # Aquí registraríamos el log si existiera,
        # pero para que no falle la petición principal dejamos pasar el error si no se pudo borrar
        pass