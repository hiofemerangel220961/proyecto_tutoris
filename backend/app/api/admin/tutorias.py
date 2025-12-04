from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db
from ...models.usuario import Usuario

router = APIRouter(prefix="/admin", tags=["admin-tutorias"])

# Igual que en otras vistas
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/tutorias/{tutoria_id}")
def ver_detalle_tutoria(
    request: Request,
    tutoria_id: int,
    db: Session = Depends(get_db),
):
    # Admin de prueba (Tulio)
    user = (
        db.query(Usuario)
        .filter(Usuario.correo == "admin@tutorias.com")
        .first()
    )

    # 🔹 Datos de prueba para que la pantalla se vea como el Figma
    tutoria = {
        "tutor_nombre": "Juan Carlos Bodoque",
        "ambiente": "101",
        "semestre": "2025-II",
        "fecha": "10/12/2025",
        "resumen": "Tutoria de seguimiento a estudiantes",
        "detalles": "Lorem ipsum de prueba para ver el diseño de la pantalla.",
    }

    sesiones = [
        {
            "estudiante_nombre": "Mario Hugo",
            "escuela": "Ing. Informática y de Sistemas",
            "asistio": "Sí",
            "derivacion_psico": "No",
        },
        {
            "estudiante_nombre": "Mario Hugo",
            "escuela": "Ing. Informática y de Sistemas",
            "asistio": "Sí",
            "derivacion_psico": "No",
        },
    ]

    return templates.TemplateResponse(
        "admin/detalle_tutoria.html",
        {
            "request": request,
            "user": user,
            "tutoria": tutoria,
            "sesiones": sesiones,
        },
    )


@router.get("/sesion/{sesion_id}")
def ver_detalle_sesion(
    request: Request,
    sesion_id: int,
    db: Session = Depends(get_db),
):
    # Admin de prueba (Tulio)
    user = (
        db.query(Usuario)
        .filter(Usuario.correo == "admin@tutorias.com")
        .first()
    )

    # 🔹 Mock Data for Session Detail
    sesion = {
        "id": sesion_id,
        "fecha": "20/10/2025",
        "semestre": "2025-II",
        "ambiente": "201",
        "derivacion": "No",
        "tutor": {
            "nombres": "Juan Carlos",
            "apellidos": "Bodoque",
            "dni": "67895432",
            "correo": "BodoqueJuan@gmail.com",
            "telefono": "925297345",
            "ambiente": "Cubil 045"
        },
        "tutorado": {
            "nombres": "Mario Hugo",
            "apellidos": "Bodoque",
            "dni": "67895432",
            "correo": "BodoqueJuan@gmail.com",
            "telefono": "925297345",
            "fecha_nacimiento": "20/10/2005"
        },
        "acuerdos": {
            "academico": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
            "personal": "Acuerdos personales de prueba...",
            "profesional": "Acuerdos profesionales de prueba..."
        },
        "observaciones": {
            "academico": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
            "personal": "Observaciones personales de prueba...",
            "profesional": "Observaciones profesionales de prueba..."
        }
    }

    return templates.TemplateResponse(
        "admin/sesion_detalle.html",
        {
            "request": request,
            "user": user,
            "sesion": sesion,
        },
    )
