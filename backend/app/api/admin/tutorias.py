from datetime import datetime
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pathlib import Path

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...models.carrera import Carrera
from ...models.semestre import Semestre
from ...models.bloque_programacion_tutorias import BloqueProgramacionTutorias

router = APIRouter(prefix="/admin", tags=["admin-tutorias"])

# Igual que en otras vistas
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/tutorias/programar")
def ver_programar_tutoria(
    request: Request,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Carreras (para el select)
    carreras = db.query(Carrera).filter(Carrera.activo == True).all()

    return templates.TemplateResponse(
        "admin/programar_tutoria.html",
        {
            "request": request,
            "user": usuario,
            "carreras": carreras,
            "active_page": "programar" # Para resaltar en sidebar
        }
    )

@router.post("/tutorias/programar")
def guardar_programacion_tutoria(
    request: Request,
    carrera_id: int = Form(...),
    fecha_inicio: str = Form(...),
    fecha_fin: str = Form(...),
    resumen: str = Form(None),
    descripcion: str = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Admin Mock (el creador)
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    
    # 2. Obtener semestre activo (o el más reciente)
    semestre_act = db.query(Semestre).order_by(Semestre.id.desc()).first()

    # 3. Crear Bloque de Programación
    try:
        nuevo_bloque = BloqueProgramacionTutorias(
            id_carrera=carrera_id,
            id_semestre=semestre_act.id if semestre_act else None,
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
            fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d'),
            resumen=resumen,
            descripcion=descripcion,
            estado="ACTIVO",
            creado_por=usuario.id_usuario,
            fecha_creacion=datetime.now()
        )
        db.add(nuevo_bloque)
        db.commit()
    except Exception as e:
        db.rollback()
        # En una app real, mostraríamos un error en el form.
        print("Error creando bloque:", e)

    # 4. Redirigir a listado (o dashboard por ahora)
    return RedirectResponse(url="/admin/dashboard", status_code=303)
