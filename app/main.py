# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import get_settings
from app.database import verify_connection, engine
from app.models import Base

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al INICIAR el servidor
    print("🚀 Iniciando Torteria API...")
    verify_connection()
    Base.metadata.create_all(bind=engine)
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    yield
    # Código que corre al DETENER el servidor
    print("🛑 Deteniendo Torteria API...")


app = FastAPI(
    title="Torteria API",
    description="API para gestión de menú, órdenes y estadísticas de la tortería",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — permite que el frontend (React) pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # puerto de Vite (React)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir imágenes subidas como archivos estáticos
app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_FOLDER),
    name="uploads",
)


# Endpoint de salud — útil para verificar que el servidor corre
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": "Torteria API",
        "version": "1.0.0",
    }