from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from ...db.deps import get_db
from ...services.semestre import SemestreService
from ...schemas.semestre import SemestreRead, SemestreCreate
from ...models.usuario import Usuario  # <--- Importamos el modelo Usuario
from backend.app.services.clase import ClaseService
from backend.app.models.semestre import Semestre
from backend.app.models.carrera import Carrera


router = APIRouter()

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/dashboard")
def admin_dashboard(
    request: Request, 
    db: Session = Depends(get_db),
    search: Optional[str] = None,       # Parámetro de búsqueda
    carrera_id: Optional[int] = None    # Parámetro de filtro
):
    # 1. Obtener Admin (Tulio)
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Semestre Activo (o el último creado si no hay activos)
    # Buscamos uno que esté ACTIVO
    semestre_actual = db.query(Semestre).filter(Semestre.activo == True).first()
    
    # Si no hay activo, tomamos el último creado para que no salga error (modo prueba)
    if not semestre_actual:
        semestre_actual = db.query(Semestre).order_by(Semestre.anio.desc(), Semestre.periodo.desc()).first()

    # 3. Listar Carreras (para el filtro desplegable)
    carreras = db.query(Carrera).filter(Carrera.activo == True).all()

    # 4. Obtener las Clases (usando el servicio nuevo)
    clases = []
    if semestre_actual:
        clases = ClaseService.get_dashboard_clases(
            db, 
            semestre_id=semestre_actual.id, 
            search=search, 
            carrera_id=carrera_id
        )

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "user": usuario,
        "semestre": semestre_actual,
        "carreras": carreras,
        "clases": clases,
        "filters": {"search": search, "carrera_id": carrera_id} # Para mantener lo que escribió el usuario
    })
