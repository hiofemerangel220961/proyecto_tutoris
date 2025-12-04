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

# RUTAS COMENTADAS PARA EVITAR CONFLICTOS CON CLASES.PY
# @router.get("/tutorias/{tutoria_id}")
# def ver_detalle_tutoria(...): ...

# @router.get("/sesion/{sesion_id}")
# def ver_detalle_sesion(...): ...
