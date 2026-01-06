from pathlib import Path
from typing import Optional

from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
from uuid import uuid4
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select


from ...db.deps import get_db
from ...models.usuario import Usuario
from ...models.semestre import Semestre
from ...models.clase_tutoria import ClaseTutoria
from ...models.carrera import Carrera

# Ruta de templates (puedes ajustarla si quieres usar la absoluta)
templates = Jinja2Templates(directory="frontend/templates")
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"
UPLOAD_DIR = STATIC_DIR / "uploads" / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    email: Optional[str] = None,
    search: Optional[str] = None,
    carrera_id: Optional[int] = None,
):
    """
    Dashboard del administrador:
    - Obtiene semestre activo
    - Lista clases activas
    - Filtro por carrera
    - Buscador por nombre del tutor
    """

    # 👉 Admin actual (por query param o por defecto)
    admin_email = email or "admin@tutorias.com"
    admin = (
        db.query(Usuario)
        .filter(Usuario.correo == admin_email)
        .first()
    )

    # 1. Obtener semestre activo
    semestre = (
        db.execute(
            select(Semestre)
            .where(Semestre.activo == True)
            .order_by(Semestre.anio.desc())
        )
        .scalars()
        .first()
    )

    if not semestre:
        return templates.TemplateResponse(
            "admin/dashboard.html",
            {
                "request": request,
                "user": admin,
                "semestre": None,
                "clases": [],
                "carreras": [],
                "filters": {
                    "search": search,
                    "carrera_id": carrera_id,
                }
            },
        )

    # 2. Base de consulta: clases activas en ese semestre
    stmt = (
        select(ClaseTutoria)
        .where(
            ClaseTutoria.id_semestre == semestre.id,
            ClaseTutoria.activo == True,
        )
        .join(ClaseTutoria.tutor)
        .join(ClaseTutoria.ambiente, isouter=True)
        .join(ClaseTutoria.semestre)
    )

    # 3. Buscador de tutor (por nombres/apellidos)
    if search:
        search_term = f"%{search}%"
        # Ojo: aquí asumo que el nombre del tutor está en Usuario asociado al Tutor
        stmt = stmt.join(ClaseTutoria.tutor).join(Usuario).where(
            (Usuario.nombres.ilike(search_term))
            | (Usuario.apellidos.ilike(search_term))
        )

    # 4. Filtro por carrera
    if carrera_id:
        stmt = stmt.join(ClaseTutoria.tutor).where(
            ClaseTutoria.tutor.has(Carrera.id == carrera_id)
        )

    clases = db.execute(stmt).scalars().all()

    # 5. Todas las carreras para el dropdown
    carreras = db.execute(
        select(Carrera).where(Carrera.activo == True).order_by(Carrera.nombre)
    ).scalars().all()

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "user": admin,
            "semestre": semestre,
            "clases": clases,
            "carreras": carreras,
            "filters": {
                "search": search or "",
                "carrera_id": carrera_id,
            },
        },
    )
@router.post("/perfil/foto")
async def subir_foto_perfil(
    foto: UploadFile = File(...),   # ✅ ahora se llama "foto"
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ext = Path(foto.filename).suffix.lower()
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Formato no permitido (jpg, png, webp)")

    filename = f"user_{usuario.id_usuario}_{uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename

    content = await foto.read()
    with open(filepath, "wb") as f:
        f.write(content)

    usuario.foto_perfil_url = f"/static/uploads/avatars/{filename}"
    db.commit()
    db.refresh(usuario)

    return {"ok": True, "foto_perfil_url": usuario.foto_perfil_url}