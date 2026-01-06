from pathlib import Path
from typing import List, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...models.tutor import Tutor
from ...models.semestre import Semestre
from ...models.clase_tutoria import ClaseTutoria
from ...models.asignacion_tutorado import AsignacionTutorado
from ...models.sesion_programada import SesionProgramada
from ...models.sesion_tutoria import SesionTutoria

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()


@router.get("/dashboard")
def tutor_dashboard(request: Request, db: Session = Depends(get_db), email: str = "tutor@tutorias.com"):
    # ⚠️ Por ahora: “tutor loggeado” vía query param (o por defecto)
    user = db.query(Usuario).filter(Usuario.correo == email).first()

    tutor = None
    semestre = None
    clase = None
    sesiones_programadas: List[SesionProgramada] = []
    tutorados: List[Dict] = []
    ambiente_str = "N/A"

    if user:
        tutor = db.query(Tutor).filter(Tutor.id_usuario == user.id_usuario).first()

        semestre = (
            db.query(Semestre)
            .filter(Semestre.activo == True)
            .order_by(Semestre.anio.desc())
            .first()
        )

        if tutor and semestre:
            clase = (
                db.query(ClaseTutoria)
                .join(ClaseTutoria.semestre)
                .filter(
                    ClaseTutoria.id_tutor == tutor.id,
                    ClaseTutoria.activo == True,
                    Semestre.activo == True,
                )
                .first()
            )

            # Ambiente mostrado
            if clase and clase.ambiente:
                ambiente_str = f"{clase.ambiente.nombre}"
            elif tutor and tutor.id_ambiente_defecto:
                ambiente_str = "Ambiente asignado"

            # Sesiones programadas (cards)
            sesiones_programadas = (
                db.query(SesionProgramada)
                .join(SesionProgramada.clase)
                .join(ClaseTutoria.semestre)
                .filter(
                    SesionProgramada.id_tutor == tutor.id,
                    SesionProgramada.estado == "PROGRAMADA",
                    Semestre.activo == True,
                )
                .order_by(SesionProgramada.fecha_hora_inicio.asc())
                .all()
            )

            # Tutorados
            if clase:
                asignaciones = (
                    db.query(AsignacionTutorado)
                    .filter(
                        AsignacionTutorado.id_clase == clase.id,
                        AsignacionTutorado.estado == "VIGENTE",
                    )
                    .all()
                )

                student_ids = [a.id_estudiante for a in asignaciones]
                counts = {}
                if student_ids:
                    rows = (
                        db.query(SesionTutoria.id_estudiante, func.count(SesionTutoria.id))
                        .filter(
                            SesionTutoria.id_tutor == tutor.id,
                            SesionTutoria.id_estudiante.in_(student_ids),
                        )
                        .group_by(SesionTutoria.id_estudiante)
                        .all()
                    )
                    counts = {sid: c for sid, c in rows}

                for a in asignaciones:
                    est = a.estudiante
                    tutorados.append(
                        {
                            "estudiante": est,
                            "carrera": est.carrera,
                            "sesiones": counts.get(est.id, 0),
                        }
                    )

    return templates.TemplateResponse(
        "tutor/dashboard.html",
        {
            "request": request,
            "user": user,
            "tutor": tutor,
            "semestre": semestre,
            "clase": clase,
            "ambiente_str": ambiente_str,
            "sesiones_programadas": sesiones_programadas,
            "tutorados": tutorados,
            "active_page": "dashboard",
        },
    )


@router.get("/sesiones/nueva")
def tutor_nueva_sesion(request: Request):
    return templates.TemplateResponse(
        "tutor/placeholder.html",
        {"request": request, "active_page": "nueva_sesion", "titulo": "Iniciar nueva sesión"},
    )


@router.get("/configuracion")
def tutor_configuracion(request: Request):
    return templates.TemplateResponse(
        "tutor/placeholder.html",
        {"request": request, "active_page": "configuracion", "titulo": "Configuración"},
    )


@router.get("/perfil")
def tutor_perfil(request: Request):
    return templates.TemplateResponse(
        "tutor/placeholder.html",
        {"request": request, "active_page": "perfil", "titulo": "Editar perfil (pendiente)"},
    )


@router.get("/tutorados/{estudiante_id}")
def tutor_tutorado_detalle(request: Request, estudiante_id: int):
    return templates.TemplateResponse(
        "tutor/placeholder.html",
        {
            "request": request,
            "active_page": "dashboard",
            "titulo": f"Detalle de tutorado {estudiante_id} (pendiente)",
        },
    )


@router.get("/sesiones/programadas/{sesion_id}/iniciar")
def tutor_iniciar_sesion_programada(request: Request, sesion_id: int):
    return templates.TemplateResponse(
        "tutor/placeholder.html",
        {
            "request": request,
            "active_page": "dashboard",
            "titulo": f"Iniciar sesión programada {sesion_id} (pendiente)",
        },
    )
