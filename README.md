# Torteria Backend API

API REST construida con **FastAPI** para la gestión de menú, órdenes y estadísticas de una tortería.

## Tecnologías

* **Python 3.12** — Lenguaje principal
* **FastAPI** — Framework web de alto rendimiento
* **SQLAlchemy** — ORM para interacción con la base de datos
* **MariaDB** — Sistema de gestión de base de datos
* **JWT** — Estándar para autenticación segura
* **Pillow** — Procesamiento y validación de imágenes

## Requisitos

* Python 3.10+
* MariaDB corriendo localmente
* Base de datos `torteria` creada previamente

## Instalación

```bash
# Clonar el repositorio
git clone [https://github.com/tuusuario/torteria-backend.git](https://github.com/tuusuario/torteria-backend.git)
cd torteria-backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
````

## Configuración

Edita el archivo `.env` con los siguientes parámetros:

Fragmento de código

```css
DB_HOST=localhost
DB_PORT=3306
DB_NAME=torteria
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
SECRET_KEY=una_clave_secreta_segura
DEBUG=True
UPLOAD_FOLDER=uploads
MAX_IMAGE_SIZE_MB=5
```

## Ejecutar

Bash

```shell
uvicorn app.main:app --reload
```

> **Nota:** La documentación interactiva (Swagger UI) estará disponible en: `http://localhost:8000/docs`

## Endpoints principales

|**Método**|**Endpoint**|**Auth**|**Descripción**|
|---|---|---|---|
|POST|`/auth/login`|No|Iniciar sesión y obtener token|
|GET|`/auth/me`|Sí|Obtener datos del usuario actual|
|GET|`/categories/`|No|Listar todas las categorías|
|POST|`/categories/`|Admin|Crear una nueva categoría|
|GET|`/products/`|No|Listar todos los productos|
|POST|`/products/`|Admin|Crear un nuevo producto|
|POST|`/products/{id}/image`|Admin|Subir imagen del producto|
|POST|`/orders/`|No|Crear una nueva orden|
|GET|`/orders/`|Admin|Listar historial de órdenes|
|PUT|`/orders/{id}`|Admin|Actualizar estado de la orden|
|GET|`/stats/`|Admin|Obtener reporte de estadísticas|

## Tests

Bash

```shell
pytest tests/ -v
```

## Estructura del proyecto

```css
torteria-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── utils/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── tests/
├── uploads/
├── requirements.txt
└── .env.example
```
