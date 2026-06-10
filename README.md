# Plantilla FastAPI + MySQL

Plantilla lista para usar como base de proyectos web con Python. Incluye conexión a MySQL, documentación automática y un ejemplo de CRUD completo.

---

## ¿Qué es esto?

Un proyecto base con la estructura mínima para construir una **API REST** usando:

- **FastAPI** — framework web moderno para Python
- **MySQL** — base de datos relacional

Una **API** es un servidor que recibe peticiones y devuelve datos (generalmente JSON). Tu frontend (web, app móvil, etc.) se conecta a esta API para mostrar y guardar información.

---

## Requisitos previos

- Python 3.10 o superior → [descargar](https://www.python.org/downloads/)
- MySQL corriendo en tu máquina (XAMPP, WAMP, o instalación directa)
- Una terminal (PowerShell en Windows, Terminal en Mac/Linux)

---

## Instalación paso a paso

### 1. Cloná o descargá el proyecto

```bash
git clone <url-del-repo>
cd fast-api-base
```

### 2. Creá un entorno virtual

Un entorno virtual es una carpeta donde se instalan las librerías de este proyecto sin afectar al resto de tu sistema.

```bash
# Crear el entorno
python -m venv venv

# Activarlo (Windows)
venv\Scripts\activate

# Activarlo (Mac / Linux)
source venv/bin/activate
```

Cuando el entorno está activo, vas a ver `(venv)` al inicio de tu terminal.

### 3. Instalá las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurá la base de datos

Copiá el archivo `.env.example` y renombralo a `.env`:

```bash
# Mac / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Abrí el archivo `.env` y completá con tus datos:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=tu_contraseña
DB_NAME=mi_base
```

> **Importante:** el archivo `.env` nunca debe subirse a GitHub. Ya está incluido en `.gitignore` para protegerlo.

### 5. Creá las tablas en MySQL

Abrí MySQL (phpMyAdmin, MySQL Workbench o terminal) y ejecutá el contenido del archivo **`schema.sql`**.

El archivo ya tiene todo listo: crea la base de datos y las tablas necesarias.

```bash
# Opción rápida desde terminal:
mysql -u root -p < schema.sql
```

---

## Correr el proyecto

```bash
uvicorn main:app --reload
```

Si todo está bien, vas a ver algo así:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Abrí tu navegador y entrá a **http://localhost:8000/docs** para ver la documentación interactiva (Swagger).

---

## Documentación automática

FastAPI genera documentación automática a partir de tu código:

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000/docs` | Swagger — podés probar los endpoints directamente |
| `http://localhost:8000/redoc` | ReDoc — documentación más prolija para leer |

---

## Endpoints del ejemplo

| Método | URL | Qué hace |
|--------|-----|----------|
| GET | `/alumnos/` | Lista todos los alumnos |
| GET | `/alumnos/{id}` | Trae un alumno por su ID |
| POST | `/alumnos/` | Crea un alumno nuevo |
| PUT | `/alumnos/{id}` | Actualiza un alumno existente |
| DELETE | `/alumnos/{id}` | Elimina un alumno |

**Ejemplo de JSON para POST/PUT:**
```json
{
  "nombre": "Ana",
  "apellido": "García",
  "email": "ana@mail.com",
  "grado": 3
}
```

---

## Estructura del proyecto

```
fast-api-base/
├── main.py        ← Punto de entrada. Configuración general de la app.
├── connect.py     ← Conexión a MySQL. No hace falta tocarlo.
├── schema.sql     ← Ejecutar UNA VEZ para crear las tablas en MySQL.
├── rutas/
│   └── alumnos.py ← Endpoints de la tabla "alumnos" (copiarlo para cada tabla nueva)
├── .env           ← Tus credenciales (no subir a GitHub)
├── .env.example   ← Plantilla del .env (sí se puede subir)
├── requirements.txt
└── .gitignore
```

---

## ¿Cómo agrego una nueva tabla?

Supongamos que querés agregar una tabla `productos`.

### Paso 1 — Agregar la tabla en `schema.sql`

Abrí `schema.sql` y agregá al final:

```sql
CREATE TABLE IF NOT EXISTS productos (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio DECIMAL(10, 2),
    stock  INT DEFAULT 0
);
```

Ejecutalo en MySQL para crear la tabla.

### Paso 2 — Crear las rutas en `rutas/productos.py`

Copiá `rutas/alumnos.py`, renombralo a `productos.py` y reemplazá:
- `alumnos` → `productos` en los nombres de funciones y el prefix del router
- Los campos en los SQL (`nombre`, `apellido`, etc.) por los de tu tabla
- El nombre de la tabla en cada `cursor.execute(...)`

### Paso 3 — Registrar el router en `main.py`

Agregá estas dos líneas en `main.py`:

```python
from rutas import productos           # al inicio, junto a los otros imports
app.include_router(productos.router)  # debajo del include_router de alumnos
```

¡Listo! Tus nuevos endpoints van a aparecer automáticamente en `/docs`.

---

## Errores frecuentes

| Error | Solución |
|-------|----------|
| `Can't connect to MySQL` | Verificá que MySQL esté corriendo y que los datos en `.env` sean correctos |
| `ModuleNotFoundError` | Activá el entorno virtual y ejecutá `pip install -r requirements.txt` |
| `Table doesn't exist` | Ejecutá `schema.sql` en tu base de datos |
| `Address already in use` | Cambiá el puerto: `uvicorn main:app --reload --port 8001` |
