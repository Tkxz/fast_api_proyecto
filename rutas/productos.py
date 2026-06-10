"""
rutas/productos.py — Endpoints para la tabla "productos"
======================================================
Cada función de este archivo es un ENDPOINT (una URL de la API).
FastAPI asocia automáticamente cada función con su método HTTP
(GET, POST, PUT, DELETE) y su URL.

MÉTODOS HTTP:
  GET    → obtener datos (no modifica nada)
  POST   → crear un registro nuevo
  PUT    → actualizar un registro existente
  DELETE → eliminar un registro

PARA AGREGAR UNA NUEVA TABLA:
  1. Copiá este archivo y renombralo (ej: productos.py)
  2. Cambiá "productos" por el nombre de tu tabla en los SQL
  3. Registrá el nuevo router en main.py
"""

from fastapi import APIRouter, HTTPException, Request

from connect import get_conexion

# APIRouter agrupa todos los endpoints de este archivo.
# prefix: todas las URLs de acá empiezan con /productos
# tags:   agrupa los endpoints en la documentación de Swagger
router = APIRouter(prefix="/productos", tags=["productos"])

# ─────────────────────────────────────────────
#  GET /productos/  →  Lista todos los productos
# ─────────────────────────────────────────────
@router.get("/")
def listar_productos():
    """Devuelve la lista completa de productos."""
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM productos")
        resultado = cursor.fetchall()   # fetchall → lista de filas
    conexion.close()
    return resultado


# ─────────────────────────────────────────────
#  GET /productos/{id}  →  Un producto por su ID
# ─────────────────────────────────────────────
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    """
    Devuelve un producto según su ID.
    Si no existe, responde con error 404.
    """
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        # %s es un placeholder seguro — evita SQL injection
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        alumno = cursor.fetchone()   # fetchone → una sola fila o None
    conexion.close()

    if alumno is None:
        # HTTPException le dice a FastAPI que responda con un código de error
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    return alumno


# ─────────────────────────────────────────────
#  POST /productos/  →  Crea un producto nuevo
# ─────────────────────────────────────────────
@router.post("/")
async def crear_producto(request: Request):
    """
    Crea un producto nuevo en la base de datos.
    Recibe un JSON con los datos del producto:
      { "nombre": "Ana", "marca": "García", "precio": 100.00, "stock": 10 }
    """
    # request.json() lee el cuerpo de la petición como diccionario
    datos = await request.json()

    conexion = get_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        cursor.execute(sql, (datos["nombre"], datos.get("precio"), datos.get("stock")))
        conexion.commit()           # commit guarda los cambios en la BD
        nuevo_id = cursor.lastrowid # id que asignó la base de datos
    conexion.close()

    return {"id": nuevo_id, **datos}


# ─────────────────────────────────────────────
#  PUT /productos/{id}  →  Actualiza un producto
# ─────────────────────────────────────────────
@router.put("/{producto_id}")
async def actualizar_producto(producto_id: int, request: Request):
    """
    Actualiza los campos enviados de un producto existente.
    Solo se modifican los campos que vengan en el JSON.
    Si el producto no existe, responde con error 404.
    """
    datos = await request.json()

    if not datos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    # Construimos el SET del UPDATE solo con los campos que llegaron
    set_clause = ", ".join(f"{campo} = %s" for campo in datos)
    valores = list(datos.values()) + [producto_id]

    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"UPDATE productos SET {set_clause} WHERE id = %s", valores)
        conexion.commit()
        filas_afectadas = cursor.rowcount

    if filas_afectadas == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Traemos el registro actualizado para devolverlo
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        alumno_actualizado = cursor.fetchone()
    conexion.close()

    return alumno_actualizado


# ─────────────────────────────────────────────
#  DELETE /productos/{id}  →  Elimina un alumno
# ─────────────────────────────────────────────
@router.delete("/{producto_id}")
def eliminar_alumno(producto_id: int):
    """
    Elimina un alumno por su ID.
    Si no existe, responde con error 404.
    """
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="producto no encontrado")

    return {"mensaje": f"producto {producto_id} eliminado correctamente"}
