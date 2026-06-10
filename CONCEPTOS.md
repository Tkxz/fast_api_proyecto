# Conceptos clave: REST, HTTP y APIs

Esta guía explica los conceptos detrás del proyecto para que entiendas qué está pasando cuando corré la API, no solo cómo copiar el código.

---

## 1. ¿Qué es una API?

**API** significa *Application Programming Interface* — interfaz de programación de aplicaciones. Suena complicado, pero la idea es simple.

Pensá en un restaurante:

```
      VOS              MOZO              COCINA
   (cliente)          (API)          (base de datos)

  "Quiero una       "Mesa 5 pide      [prepara el
   milanesa"   →     milanesa"   →     plato]
                         ←
                  "Acá tiene"    ←   [plato listo]
```

- **Vos** sos el cliente (el navegador, una app, Swagger)
- **El mozo** es la API (FastAPI en este proyecto)
- **La cocina** es la base de datos (MySQL)

El cliente nunca toca directamente la cocina. Todo pasa por el mozo. Eso es una API.

---

## 2. ¿Qué es REST?

**REST** no es un programa ni una librería. Es un conjunto de *convenciones* (reglas acordadas) para organizar una API de forma ordenada.

La regla principal de REST es:

> Cada "cosa" del sistema tiene su propia URL, y las operaciones sobre esa cosa se expresan con el método HTTP.

En este proyecto, la "cosa" son los alumnos:

```
/alumnos/       → todos los alumnos
/alumnos/5      → el alumno con id = 5
/alumnos/12     → el alumno con id = 12
```

Una API que sigue estas convenciones se llama **API REST** o **API RESTful**.

---

## 3. El protocolo HTTP

**HTTP** es el "idioma" con el que se comunican cliente y servidor en la web. Cuando entrás a una página web, tu navegador habla HTTP con el servidor.

Toda comunicación HTTP tiene dos partes:

### La petición (lo que manda el cliente)
```
MÉTODO   URL              CUERPO (opcional)
GET      /alumnos/
POST     /alumnos/        {"nombre": "Ana", "apellido": "García"}
DELETE   /alumnos/5
```

### La respuesta (lo que devuelve el servidor)
```
CÓDIGO   CUERPO
200      [{"id": 1, "nombre": "Ana", ...}, ...]
404      {"detail": "Alumno no encontrado"}
```

---

## 4. Los métodos HTTP (los "verbos")

Los métodos HTTP son como verbos — dicen *qué querés hacer*. Hay cuatro que se usan en REST:

| Método   | ¿Qué hace?             | Equivalente en SQL |
|----------|------------------------|--------------------|
| `GET`    | Traer / leer datos     | `SELECT`           |
| `POST`   | Crear un registro nuevo | `INSERT`          |
| `PUT`    | Actualizar uno existente | `UPDATE`          |
| `DELETE` | Eliminar un registro   | `DELETE`           |

### Cómo se ve en el código

En `rutas/alumnos.py`, cada endpoint declara su método con un decorador:

```python
@router.get("/")          # GET    /alumnos/
def listar_alumnos():
    ...

@router.post("/")         # POST   /alumnos/
async def crear_alumno(request):
    ...

@router.put("/{id}")      # PUT    /alumnos/5
async def actualizar_alumno(alumno_id, request):
    ...

@router.delete("/{id}")   # DELETE /alumnos/5
def eliminar_alumno(alumno_id):
    ...
```

FastAPI asocia automáticamente cada función con su método y URL.

---

## 5. Las URLs y los parámetros

Una URL puede ser fija o tener partes variables:

```
/alumnos/          →  URL fija      → afecta a TODOS los alumnos
/alumnos/5         →  URL variable  → afecta SOLO al alumno con id 5
/alumnos/12        →  URL variable  → afecta SOLO al alumno con id 12
```

En el código, la parte variable se escribe entre llaves:

```python
@router.get("/{alumno_id}")
def obtener_alumno(alumno_id: int):
    #             ↑
    #  FastAPI captura el número de la URL
    #  y lo pasa como parámetro a la función
```

Si entrás a `http://localhost:8000/alumnos/7`, FastAPI ejecuta `obtener_alumno(alumno_id=7)` automáticamente.

---

## 6. El cuerpo de la petición y JSON

Cuando querés *enviar datos* al servidor (crear o actualizar algo), los datos van en el **cuerpo** de la petición. El formato estándar que se usa es **JSON**.

**JSON** es texto estructurado con llaves, claves y valores:

```json
{
  "nombre": "Ana",
  "apellido": "García",
  "email": "ana@mail.com",
  "grado": 3
}
```

Reglas básicas de JSON:
- Las claves van entre comillas dobles: `"nombre"`
- Los textos van entre comillas: `"Ana"`
- Los números van sin comillas: `3`
- Los campos se separan con coma

### Cómo llegan esos datos al código

En los endpoints que reciben datos (`POST` y `PUT`), el código lee el JSON así:

```python
async def crear_alumno(request: Request):
    datos = await request.json()
    #               ↑
    #  Lee el JSON del cuerpo de la petición
    #  y lo convierte en un diccionario de Python

    nombre   = datos["nombre"]     # "Ana"
    apellido = datos["apellido"]   # "García"
    grado    = datos.get("grado")  # 3  (o None si no se envió)
```

---

## 7. Los códigos de respuesta HTTP

Cada respuesta HTTP incluye un **código numérico** que indica si todo salió bien o qué falló.

Los más comunes en este proyecto:

| Código | Nombre | Cuándo ocurre |
|--------|--------|---------------|
| `200`  | OK | Todo salió bien. Respuesta exitosa. |
| `201`  | Created | Se creó un registro nuevo correctamente. |
| `400`  | Bad Request | Los datos enviados tienen algún problema. |
| `404`  | Not Found | El recurso pedido no existe. |
| `500`  | Internal Server Error | Algo falló en el servidor (revisar la terminal). |

Seguramente ya viste el `404` en páginas web — es el mismo concepto.

### Cómo se genera un 404 en el código

```python
alumno = cursor.fetchone()   # busca el alumno en la BD

if alumno is None:           # si no existe...
    raise HTTPException(status_code=404, detail="Alumno no encontrado")
    #                   ↑
    #  FastAPI devuelve automáticamente:
    #  HTTP 404 + {"detail": "Alumno no encontrado"}
```

---

## 8. El ciclo completo — de click a dato

Este es el recorrido completo de una petición a través del proyecto:

```
┌─────────────────────────────────────────────────────┐
│  Cliente (Swagger, navegador, app)                  │
│                                                     │
│  GET /alumnos/5                                     │
└──────────────────────┬──────────────────────────────┘
                       │ petición HTTP
                       ▼
┌─────────────────────────────────────────────────────┐
│  main.py                                            │
│  Recibe la petición y la redirige al router         │
│  correcto según la URL                              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  rutas/alumnos.py → obtener_alumno(alumno_id=5)     │
│                                                     │
│  1. Llama a get_conexion() de connect.py            │
│  2. Ejecuta: SELECT * FROM alumnos WHERE id = 5     │
│  3. Si no existe → devuelve 404                     │
│  4. Si existe → continúa                            │
└──────────────────────┬──────────────────────────────┘
                       │ consulta SQL
                       ▼
┌─────────────────────────────────────────────────────┐
│  MySQL                                              │
│  Busca el alumno y devuelve la fila como dict       │
│  {"id": 5, "nombre": "Ana", ...}                    │
└──────────────────────┬──────────────────────────────┘
                       │ resultado
                       ▼
┌─────────────────────────────────────────────────────┐
│  rutas/alumnos.py                                   │
│  Recibe el dict y lo retorna                        │
└──────────────────────┬──────────────────────────────┘
                       │ respuesta HTTP 200 + JSON
                       ▼
┌─────────────────────────────────────────────────────┐
│  Cliente                                            │
│  {"id": 5, "nombre": "Ana", "apellido": "García"}  │
└─────────────────────────────────────────────────────┘
```

---

## 9. ¿Qué hace cada archivo?

| Archivo | Rol en el ciclo |
|---------|----------------|
| `main.py` | Crea la app y decide a qué router mandar cada petición según la URL |
| `connect.py` | Sabe cómo conectarse a MySQL. Provee `get_conexion()` |
| `rutas/alumnos.py` | Define qué hacer con cada petición de `/alumnos/...` |
| `schema.sql` | Define la estructura de la base de datos (se ejecuta una sola vez) |
| `.env` | Guarda las credenciales de la base de datos de forma segura |

---

## Resumen rápido

```
REST     = convención para organizar URLs y métodos
HTTP     = protocolo de comunicación web (petición → respuesta)
Método   = GET / POST / PUT / DELETE  (qué querés hacer)
URL      = dónde querés hacerlo  (/alumnos/5)
JSON     = formato de los datos que se envían y reciben
Código   = número que indica si salió bien (200) o qué falló (404)
FastAPI  = el framework que une todo esto en Python
```
