# app/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Construir la URL de conexión
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    f"?charset=utf8mb4"
)

# Motor de conexión
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,        # muestra las queries SQL en consola (útil en desarrollo)
    pool_pre_ping=True,         # verifica la conexión antes de usarla
    pool_recycle=3600,          # recicla conexiones cada hora
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base para los modelos ORM
Base = declarative_base()


# Dependencia para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Función para verificar la conexión al iniciar
def verify_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexión a MariaDB exitosa")
    except Exception as e:
        print(f"❌ Error al conectar a MariaDB: {e}")
        raise