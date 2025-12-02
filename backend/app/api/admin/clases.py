from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...services.clase import ClaseService

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
