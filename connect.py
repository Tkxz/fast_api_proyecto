"""
connect.py — Conexión a la base de datos MySQL
================================================
Este archivo maneja TODA la conexión a la base de datos.
Los datos sensibles (usuario, contraseña, etc.) se leen
desde el archivo .env para no exponerlos en el código.

USO NORMAL (en tus rutas):
  from connect import get_conexion

  def mi_funcion():
      conexion = get_conexion()
      with conexion.cursor() as cursor:
          cursor.execute("SELECT * FROM tabla")
          resultado = cursor.fetchall()
      conexion.close()
      return resultado
"""

import os
from typing import Callable, Any

import pymysql.cursors
from pymysql import Connection
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno del sistema
load_dotenv()

# Lee las credenciales desde el archivo .env
# Si alguna variable no existe en .env, toma el valor por defecto indicado
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "")


def get_conexion():
    """
    Abre y devuelve una conexión a la base de datos.
    Usá esta función al inicio de cada endpoint que necesite la BD.
    Acordate de llamar conexion.close() cuando termines.
    """
    return pymysql.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        charset='utf8mb4',
        # DictCursor hace que cada fila sea un diccionario
        # en vez de una tupla: {"id": 1, "nombre": "Ana"}
        cursorclass=pymysql.cursors.DictCursor
    )


# ─── Modo avanzado (opcional) ────────────────────────────────────────────────
# El decorador de abajo hace lo mismo que get_conexion() pero de forma
# automática. Está acá como referencia para cuando quieran profundizar.

def dbConnectionDecorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador que abre una conexión a MySQL, la pasa a la función
    decorada y la cierra automáticamente al terminar.

    Uso:
        @dbConnectionDecorator
        def obtener_datos(conexion):
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tabla")
                return cursor.fetchall()
    """
    def wrapper(*args, **kwargs) -> Connection | str:
        try:
            conexion = pymysql.connect(
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                charset='utf8mb4',
                # DictCursor hace que cada fila sea un diccionario
                # en vez de una tupla: {"id": 1, "nombre": "Ana"}
                cursorclass=pymysql.cursors.DictCursor
            )
            result = func(conexion, *args, **kwargs)
            return result
        except Exception as e:
            # Si algo falla, devuelve el mensaje de error como texto
            return str(e)
    return wrapper