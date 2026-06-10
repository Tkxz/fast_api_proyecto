"""
main.py — Punto de entrada de la aplicación
============================================
Este es el archivo principal. Acá se crea la app de FastAPI,
se configura y se registran todos los routers (grupos de endpoints).

CÓMO CORRER EL PROYECTO:
  uvicorn main:app --reload

  --reload hace que el server se reinicie automáticamente
  cada vez que guardás un archivo. Muy útil para desarrollar.

CÓMO VER LA DOCUMENTACIÓN:
  Abrí tu navegador y andá a:
    http://localhost:8000/docs      ← Swagger (interactivo)
    http://localhost:8000/redoc     ← ReDoc (más prolijo)

PARA AGREGAR UNA NUEVA TABLA:
  1. Agregá la tabla nueva en schema.sql y ejecutalo en MySQL
  2. Copiá rutas/alumnos.py, renombralo y cambiá los SQL
  3. Importá el router acá abajo y agregalo con app.include_router()
"""
from rutas import productos 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rutas import alumnos
# ─────────────────────────────────────────────
#  Creación de la app
# ─────────────────────────────────────────────
app = FastAPI(
    title="Mi API con FastAPI",
    description="Plantilla base para proyectos con FastAPI y MySQL",
    version="1.0.0",
)

# ─────────────────────────────────────────────
#  CORS — permite que un frontend se conecte
# ─────────────────────────────────────────────
# Si tu frontend (React, Vue, HTML puro) está en otro puerto,
# necesitás habilitar CORS. En desarrollo dejamos todo abierto.
# En producción deberías poner solo el dominio de tu frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # "*" = cualquier origen (solo para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],        # permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
#  Registro de routers
# ─────────────────────────────────────────────
# Cada router agrupa los endpoints de una tabla o recurso
app.include_router(alumnos.router)
app.include_router(productos.router)
# Para agregar más tablas, repetí el patrón:
# from rutas import productos
# app.include_router(productos.router)


# ─────────────────────────────────────────────
#  Ruta raíz — confirma que el server está vivo
# ─────────────────────────────────────────────
@app.get("/", tags=["Estado"])
def inicio():
    """Endpoint de prueba para verificar que la API está corriendo."""
    return {"estado": "ok", "mensaje": "¡La API está funcionando!"}
