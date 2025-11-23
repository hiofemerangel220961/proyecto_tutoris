from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db

router = APIRouter()

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    # Aquí iría la lógica de cargar datos (semestres, clases, etc.)
    # Por ahora solo renderizamos el template
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})