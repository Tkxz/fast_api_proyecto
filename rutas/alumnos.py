"""
rutas/alumnos.py — Endpoints para la tabla "alumnos"
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
  2. Cambiá "alumnos" por el nombre de tu tabla en los SQL
  3. Registrá el nuevo router en main.py
"""

from fastapi import APIRouter, HTTPException, Request

from connect import get_conexion

# APIRouter agrupa todos los endpoints de este archivo.
# prefix: todas las URLs de acá empiezan con /alumnos
# tags:   agrupa los endpoints en la documentación de Swagger
router = APIRouter(prefix="/alumnos", tags=["alumnos"])


# ─────────────────────────────────────────────
#  GET /alumnos/  →  Lista todos los alumnos
# ─────────────────────────────────────────────
@router.get("/")
def listar_alumnos():
    """Devuelve la lista completa de alumnos."""
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM alumnos")
        resultado = cursor.fetchall()   # fetchall → lista de filas
    conexion.close()
    return resultado


# ─────────────────────────────────────────────
#  GET /alumnos/{id}  →  Un alumno por su ID
# ─────────────────────────────────────────────
@router.get("/{alumno_id}")
def obtener_alumno(alumno_id: int):
    """
    Devuelve un alumno según su ID.
    Si no existe, responde con error 404.
    """
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        # %s es un placeholder seguro — evita SQL injection
        cursor.execute("SELECT * FROM alumnos WHERE id = %s", (alumno_id,))
        alumno = cursor.fetchone()   # fetchone → una sola fila o None
    conexion.close()

    if alumno is None:
        # HTTPException le dice a FastAPI que responda con un código de error
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    return alumno


# ─────────────────────────────────────────────
#  POST /alumnos/  →  Crea un alumno nuevo
# ─────────────────────────────────────────────
@router.post("/")
async def crear_alumno(request: Request):
    """
    Crea un alumno nuevo en la base de datos.
    Recibe un JSON con los datos del alumno:
      { "nombre": "Ana", "apellido": "García", "email": "ana@mail.com", "grado": 3 }
    """
    # request.json() lee el cuerpo de la petición como diccionario
    datos = await request.json()

    conexion = get_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO alumnos (nombre, apellido, email, grado) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (datos["nombre"], datos["apellido"], datos.get("email"), datos.get("grado")))
        conexion.commit()           # commit guarda los cambios en la BD
        nuevo_id = cursor.lastrowid # id que asignó la base de datos
    conexion.close()

    return {"id": nuevo_id, **datos}


# ─────────────────────────────────────────────
#  PUT /alumnos/{id}  →  Actualiza un alumno
# ─────────────────────────────────────────────
@router.put("/{alumno_id}")
async def actualizar_alumno(alumno_id: int, request: Request):
    """
    Actualiza los campos enviados de un alumno existente.
    Solo se modifican los campos que vengan en el JSON.
    Si el alumno no existe, responde con error 404.
    """
    datos = await request.json()

    if not datos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    # Construimos el SET del UPDATE solo con los campos que llegaron
    set_clause = ", ".join(f"{campo} = %s" for campo in datos)
    valores = list(datos.values()) + [alumno_id]

    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(f"UPDATE alumnos SET {set_clause} WHERE id = %s", valores)
        conexion.commit()
        filas_afectadas = cursor.rowcount

    if filas_afectadas == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Traemos el registro actualizado para devolverlo
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM alumnos WHERE id = %s", (alumno_id,))
        alumno_actualizado = cursor.fetchone()
    conexion.close()

    return alumno_actualizado


# ─────────────────────────────────────────────
#  DELETE /alumnos/{id}  →  Elimina un alumno
# ─────────────────────────────────────────────
@router.delete("/{alumno_id}")
def eliminar_alumno(alumno_id: int):
    """
    Elimina un alumno por su ID.
    Si no existe, responde con error 404.
    """
    conexion = get_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM alumnos WHERE id = %s", (alumno_id,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    return {"mensaje": f"Alumno {alumno_id} eliminado correctamente"}
