# Sistema de Tutorías

Este proyecto es una aplicación web construida con **FastAPI** (Backend) y **Jinja2** (Frontend renderizado por el servidor).

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

1.  Clona el repositorio o navega a la carpeta del proyecto.
2.  (Opcional) Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
uvicorn backend.app.main:app --reload
```

El servidor se iniciará en `http://127.0.0.1:8000`.

## Credenciales por Defecto

Al iniciar la aplicación por primera vez, se creará un usuario administrador automáticamente:

- **Correo**: `admin@tutorias.com`
- **Contraseña**: `admin123`

## Estructura del Proyecto

- `backend/`: Código fuente del servidor FastAPI.
- `frontend/`: Plantillas HTML y archivos estáticos (CSS, JS, imágenes).
- `requirements.txt`: Lista de dependencias del proyecto.
