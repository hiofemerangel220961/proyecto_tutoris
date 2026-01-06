from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from typing import Optional
from sqlalchemy.orm import Session
from ...db.deps import get_db
from ...models.usuario import Usuario

router = APIRouter()

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/dashboard")
def verificador_dashboard(request: Request, db: Session = Depends(get_db), email: Optional[str] = None):
    # Verificador actual
    verif_email = email or "verificador@tutorias.com"
    user = db.query(Usuario).filter(Usuario.correo == verif_email).first()
    
    return templates.TemplateResponse("verificador/dashboard.html", {"request": request, "user": user})