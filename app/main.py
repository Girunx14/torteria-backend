# app/main.py — versión actualizada completa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import get_settings
from app.database import verify_connection, engine
from app.models import Base
from app.routers import auth          # ← nuevo

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando Torteria API...")
    verify_connection()
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    yield
    print("🛑 Deteniendo Torteria API...")


app = FastAPI(
    title="Torteria API",
    description="API para gestión de menú, órdenes y estadísticas",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_FOLDER),
    name="uploads",
)

# Routers
app.include_router(auth.router)       # ← nuevo


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "Torteria API", "version": "1.0.0"}