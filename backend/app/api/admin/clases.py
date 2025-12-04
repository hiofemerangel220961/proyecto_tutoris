from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...services.clase import ClaseService
from ...models.tutor import Tutor
from ...models.ambiente import Ambiente
from ...models.clase_tutoria import ClaseTutoria
from fastapi import Form
from fastapi.responses import RedirectResponse
#nuevos
from fastapi import HTTPException
# OJO: el nombre del modelo cámbialo por el TUYO
from ...models.sesion import Sesion
#-----------------

router = APIRouter()

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/clases/{clase_id}")
def ver_detalle_clase(
    request: Request, 
    clase_id: int,
    db: Session = Depends(get_db)
):
    # 1. Obtener Admin (Tulio) - Mock por ahora
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener detalle de la clase
    clase = ClaseService.get_clase_detalle(db, clase_id)
    
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    # 3. Filtrar sesiones programadas (PENDIENTES)
    sesiones_programadas = [s for s in clase.sesiones if s.estado == 'PROGRAMADA']
    
    # Ordenar por fecha ascendente (la más próxima primero)
    sesiones_programadas.sort(key=lambda x: x.fecha)

    return templates.TemplateResponse("admin/clase_detalle.html", {
        "request": request,
        "user": usuario,
        "clase": clase,
        "sesiones": sesiones_programadas # Pasamos la lista filtrada
    })



@router.get("/clases/{clase_id}/historial")
def ver_historial_clase(
    request: Request, 
    clase_id: int,
    db: Session = Depends(get_db)
):
    # 1. Obtener Admin (Tulio) - Mock por ahora
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener detalle de la clase
    clase = ClaseService.get_clase_detalle(db, clase_id)
    
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    # 3. Filtrar sesiones pasadas (REALIZADAS - HISTORIAL)
    sesiones_historial = [s for s in clase.sesiones if s.estado == 'REALIZADA']
    
    # Ordenar por fecha descendente (más reciente primero)
    sesiones_historial.sort(key=lambda x: x.fecha, reverse=True)

    return templates.TemplateResponse("admin/historial_tutorias.html", {
        "request": request,
        "user": usuario,
        "clase": clase,
        "sesiones": sesiones_historial
    })
#agregado---
@router.get("/tutorias/{sesion_id}")
def ver_detalle_tutoria(
    request: Request,
    sesion_id: int,
    db: Session = Depends(get_db)
):
    # 1. Admin “mock”
    usuario = db.query(Usuario).filter(
        Usuario.correo == "admin@tutorias.com"
    ).first()

    # 2. Buscar la sesión por id
    sesion = (
        db.query(Sesion)
        .filter(Sesion.id == sesion_id)
        .first()
    )

    if not sesion:
        raise HTTPException(status_code=404, detail="Tutoría no encontrada")

    # 3. Armar datos para el template (coinciden con tu HTML de detalle_tutoria.html)
    tutoria = {
        "tutor_nombre": f"{sesion.clase.tutor.usuario.nombres} "
                        f"{sesion.clase.tutor.usuario.apellidos}",
        "ambiente": (
            sesion.ambiente.codigo
            if sesion.ambiente
            else (sesion.clase.ambiente.codigo if sesion.clase.ambiente else "N/A")
        ),
        "semestre": (
            sesion.clase.semestre.codigo
            if sesion.clase.semestre
            else "N/A"
        ),
        "fecha": sesion.fecha.strftime("%d/%m/%Y"),
        "resumen": sesion.tema or "Sin tema",
        "detalles": getattr(sesion, "detalles", None) or "Sin detalles",
    }

    # Por ahora dejamos la lista de tutorados vacía
    sesiones_convocados = [
        {
            "id": 1,
            "estudiante_nombre": "Juan Pérez",
            "escuela": "Ingeniería Informática",
            "asistio": "Sí",
            "derivacion_psico": "No"
        }
    ]

    return templates.TemplateResponse(
        "admin/tutoria_detalle.html",
        {
            "request": request,
            "user": usuario,
            "tutoria": tutoria,
            "sesiones": sesiones_convocados,
        },
    )
#--------------------------------

@router.get("/clases/{clase_id}/editar")
def editar_clase(
    request: Request, 
    clase_id: int,
    db: Session = Depends(get_db)
):
    # 1. Obtener Admin (Tulio) - Mock por ahora
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener detalle de la clase
    clase = ClaseService.get_clase_detalle(db, clase_id)
    
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    # 3. Obtener todos los tutores y ambientes disponibles
    tutores = db.query(Tutor).join(Usuario).all()
    ambientes = db.query(Ambiente).all()

    return templates.TemplateResponse("admin/clase_editar.html", {
        "request": request,
        "user": usuario,
        "clase": clase,
        "tutores": tutores,
        "ambientes": ambientes
    })


@router.post("/clases/{clase_id}/editar")
def guardar_edicion_clase(
    request: Request,
    clase_id: int,
    tutor_id: int = Form(...),
    ambiente_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # 1. Obtener la clase
    clase = db.query(ClaseTutoria).filter(ClaseTutoria.id == clase_id).first()
    
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    # 2. Actualizar datos
    clase.id_tutor = tutor_id
    clase.id_ambiente = ambiente_id
    
    db.commit()
    
    # 3. Redirigir al detalle de la clase
    return RedirectResponse(url=f"/admin/clases/{clase_id}", status_code=303)
