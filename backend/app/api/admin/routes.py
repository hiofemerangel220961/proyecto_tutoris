from pathlib import Path
import os

from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db
from ...models.usuario import Usuario

router = APIRouter(prefix="/admin", tags=["admin"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"
AVATAR_DIR = STATIC_DIR / "uploads" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/perfil")
def ver_perfil(request: Request, db: Session = Depends(get_db)):
    # Por ahora, igual que tu proyecto: admin “mock”
    user = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    return templates.TemplateResponse(
        "admin/perfil_editar.html",
        {"request": request, "user": user, "active_page": "perfil"},
    )

@router.get("/perfil")
def ver_perfil(request: Request, db: Session = Depends(get_db)):
    admin = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    if not admin:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return templates.TemplateResponse(
        "admin/perfil.html",
        {
            "request": request,
            "user": admin,
            "active_page": "perfil",
        }
    )

@router.post("/perfil/foto")
async def subir_foto_perfil(
    request: Request,
    foto: UploadFile = File(...),          # OJO: el campo debe llamarse "foto"
    email: str | None = Form(None),        # opcional (por si luego lo usas)
    db: Session = Depends(get_db),
):
    # 1) Usuario
    user_email = email or "admin@tutorias.com"
    user = db.query(Usuario).filter(Usuario.correo == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2) Validar tipo
    if not foto.content_type or not foto.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # 3) Guardar archivo
    original_name = foto.filename or "avatar"
    _, ext = os.path.splitext(original_name)
    ext = ext.lower() if ext else ".jpg"

    filename = f"user_{user.id_usuario}{ext}"
    filepath = AVATAR_DIR / filename

    content = await foto.read()
    if len(content) > 2 * 1024 * 1024:  # 2MB (opcional)
        raise HTTPException(status_code=400, detail="Imagen muy grande (máx 2MB)")

    with open(filepath, "wb") as f:
        f.write(content)

    # 4) Guardar URL en BD (sirve porque /static está montado a frontend/static)
    user.foto_perfil_url = f"/static/uploads/avatars/{filename}"
    db.commit()

    # 5) Redirigir
    return RedirectResponse(url="/admin/perfil", status_code=303)
