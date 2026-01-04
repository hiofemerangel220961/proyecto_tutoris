from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

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
from fastapi import HTTPException
# OJO: el nombre del modelo cámbialo por el TUYO
from ...models.sesion_programada import SesionProgramada
from ...models.sesion_tutoria import SesionTutoria
from ...models.asignacion_tutorado import AsignacionTutorado
from ...models.estudiante import Estudiante
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
    sesiones = [s for s in clase.sesiones_programadas if s.estado == 'PROGRAMADA']
    
    # Ordenar por fecha ascendente (la más próxima primero)
    sesiones.sort(key=lambda x: x.fecha_hora_inicio)

    return templates.TemplateResponse("admin/clase_detalle.html", {
        "request": request,
        "user": usuario,
        "clase": clase,
        "sesiones": sesiones # Pasamos la lista filtrada
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
    sesiones_historial = [s for s in clase.sesiones_programadas if s.estado == 'REALIZADA']
    
    # Ordenar por fecha descendente (más reciente primero)
    sesiones_historial.sort(key=lambda x: x.fecha_hora_inicio, reverse=True)

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

    # 2. Buscar la sesión por id con relaciones
    sesion = (
        db.query(SesionProgramada)
        .options(
            joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.tutor).joinedload(Tutor.usuario),
            joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.semestre),
            joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.asignaciones).joinedload(AsignacionTutorado.estudiante),
            joinedload(SesionProgramada.ambiente)
        )
        .filter(SesionProgramada.id == sesion_id)
        .first()
    )

    if not sesion:
        raise HTTPException(status_code=404, detail="Tutoría no encontrada")

    return templates.TemplateResponse(
        "admin/tutoria_detalle.html",
        {
            "request": request,
            "user": usuario,
            "sesion": sesion,
        },
    )

@router.get("/tutorias/{sesion_id}/estudiante/{estudiante_id}")
def ver_detalle_sesion_individual(
    request: Request,
    sesion_id: int,
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Sesion
    sesion = (
        db.query(SesionProgramada)
        .options(
            joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.tutor).joinedload(Tutor.usuario),
            joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.semestre),
            joinedload(SesionProgramada.ambiente)
        )
        .filter(SesionProgramada.id == sesion_id)
        .first()
    )

    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    # 3. Obtener Estudiante (de la asignación)
    # Buscamos la asignación específica para validar que el estudiante pertenece a la clase
    asignacion = (
        db.query(AsignacionTutorado)
        .options(joinedload(AsignacionTutorado.estudiante))
        .filter(
            AsignacionTutorado.id_clase == sesion.id_clase,
            AsignacionTutorado.id_estudiante == estudiante_id
        )
        .first()
    )

    if not asignacion:
        raise HTTPException(status_code=404, detail="Estudiante no asignado a esta clase")

    estudiante = asignacion.estudiante

    return templates.TemplateResponse(
        "admin/sesion_detalle.html",
        {
            "request": request,
            "user": usuario,
            "sesion": sesion,
            "estudiante": estudiante
        },
    )

@router.get("/clases/{clase_id}/tutorados/{estudiante_id}")
def ver_detalle_tutorado(
    request: Request,
    clase_id: int,
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Get Class Detail
    clase = ClaseService.get_clase_detalle(db, clase_id)
    if not clase:
         raise HTTPException(status_code=404, detail="Clase no encontrada")

    # 3. Get Student Detail
    estudiante = db.query(Estudiante).options(joinedload(Estudiante.usuario)).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # 4. Get Session History
    # We fetch SesionTutoria entries for this student in this class's context
    # Or for simplicity given the current seed approach, we might just look at completed SesionProgramada
    # But ideally:
    historial_sesiones = (
        db.query(SesionProgramada)
        .filter(SesionProgramada.id_clase == clase_id)
        .filter(SesionProgramada.estado == 'REALIZADA')
        .order_by(SesionProgramada.fecha_hora_inicio.desc())
        .all()
    )

    return templates.TemplateResponse(
        "admin/tutorado_detalle.html",
        {
            "request": request,
            "user": usuario,
            "clase": clase,
            "estudiante": estudiante,
            "historial_sesiones": historial_sesiones
        },
    )

@router.get("/clases/{clase_id}/tutorados/{estudiante_id}/editar")
def editar_tutorado(
    request: Request,
    clase_id: int,
    estudiante_id: int,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Get Class & Student
    clase = ClaseService.get_clase_detalle(db, clase_id)
    if not clase:
         raise HTTPException(status_code=404, detail="Clase no encontrada")
    
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # 3. Get Tutors for dropdown
    tutores = db.query(Tutor).join(Usuario).all()

    return templates.TemplateResponse(
        "admin/tutorado_editar.html",
        {
            "request": request,
            "user": usuario,
            "clase": clase,
            "estudiante": estudiante,
            "tutores": tutores
        },
    )

@router.post("/clases/{clase_id}/tutorados/{estudiante_id}/editar")
def guardar_edicion_tutorado(
    request: Request,
    clase_id: int,
    estudiante_id: int,
    nombres: str = Form(...),
    apellidos: str = Form(...),
    dni: str = Form(...),
    codigo: str = Form(...),
    correo: str = Form(None),
    telefono: str = Form(None),
    # direccion: str = Form(None) # Not receiving this yet as not in model
    db: Session = Depends(get_db)
):
    # 1. Get Student
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # 2. Update fields
    estudiante.nombres = nombres
    estudiante.apellidos = apellidos
    estudiante.dni = dni
    estudiante.codigo = codigo
    estudiante.correo = correo
    estudiante.telefono = telefono
    
    db.commit()

    # 3. Redirect to detail
    return RedirectResponse(
        url=f"/admin/clases/{clase_id}/tutorados/{estudiante_id}",
        status_code=303
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
