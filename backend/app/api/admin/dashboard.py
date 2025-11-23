from typing import Optional

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

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
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

    # 👉 Admin actual (por ahora, el admin por defecto de init_data)
    admin = (
        db.query(Usuario)
        .filter(Usuario.correo == "admin@tutorias.com")
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
                "admin": admin,
                "semestre": None,
                "clases": [],
                "carreras": [],
                "search": search,
                "carrera_id": carrera_id,
            },
        )

    # 2. Base de consulta: clases activas en ese semestre
    stmt = (
        select(ClaseTutoria)
        .where(
            ClaseTutoria.semestre_id == semestre.id,
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
            "admin": admin,
            "semestre": semestre,
            "clases": clases,
            "carreras": carreras,
            "search": search or "",
            "carrera_id": carrera_id,
        },
    )
