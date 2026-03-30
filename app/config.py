from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Base de datos
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "torteria"
    DB_USER: str = "girun"
    DB_PASSWORD: str = ""

    # Seguridad
    SECRET_KEY: str = "cambia_esto_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 horas

    # App
    DEBUG: bool = True
    UPLOAD_FOLDER: str = "uploads"
    MAX_IMAGE_SIZE_MB: int = 5

    # Cloudinary Integración
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()