from datetime import datetime
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pathlib import Path

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...models.carrera import Carrera
from ...models.semestre import Semestre
from ...models.bloque_programacion_tutorias import BloqueProgramacionTutorias

router = APIRouter(prefix="/admin", tags=["admin-tutorias"])

# Igual que en otras vistas
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/tutorias/programar")
def ver_programar_tutoria(
    request: Request,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Carreras (para el select)
    carreras = db.query(Carrera).filter(Carrera.activo == True).all()

    return templates.TemplateResponse(
        "admin/programar_tutoria.html",
        {
            "request": request,
            "user": usuario,
            "carreras": carreras,
            "active_page": "programar" # Para resaltar en sidebar
        }
    )

@router.post("/tutorias/programar")
def guardar_programacion_tutoria(
    request: Request,
    carrera_id: int = Form(...),
    fecha_inicio: str = Form(...),
    fecha_fin: str = Form(...),
    resumen: str = Form(None),
    descripcion: str = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Admin Mock (el creador)
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    
    # 2. Obtener semestre activo (o el más reciente)
    semestre_act = db.query(Semestre).order_by(Semestre.id.desc()).first()

    # 3. Crear Bloque de Programación
    try:
        nuevo_bloque = BloqueProgramacionTutorias(
            id_carrera=carrera_id,
            id_semestre=semestre_act.id if semestre_act else None,
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
            fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d'),
            resumen=resumen,
            descripcion=descripcion,
            estado="ACTIVO",
            creado_por=usuario.id_usuario,
            fecha_creacion=datetime.now()
        )
        db.add(nuevo_bloque)
        db.commit()
    except Exception as e:
        db.rollback()
        # En una app real, mostraríamos un error en el form.
        print("Error creando bloque:", e)

    # 4. Redirigir al paso 2 (Listado de clases)
    if nuevo_bloque:
         # Obtenemos el ID generado. En SQLA el objeto se actualiza tras commit
         return RedirectResponse(
             url=f"/admin/tutorias/programar/{nuevo_bloque.id}/clases", 
             status_code=303
         )
    else:
        # Fallback si falló
        return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.get("/tutorias/programar/{bloque_id}/editar")
def ver_editar_programacion_tutoria(
    request: Request,
    bloque_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
    carreras = db.query(Carrera).filter(Carrera.activo == True).all()
    bloque = db.query(BloqueProgramacionTutorias).filter(BloqueProgramacionTutorias.id == bloque_id).first()

    return templates.TemplateResponse(
        "admin/programar_tutoria.html",
        {
            "request": request,
            "user": usuario,
            "carreras": carreras,
            "bloque": bloque,
            "active_page": "programar"
        }
    )

@router.post("/tutorias/programar/{bloque_id}/editar")
def guardar_editar_programacion_tutoria(
    request: Request,
    bloque_id: int,
    carrera_id: int = Form(...),
    fecha_inicio: str = Form(...),
    fecha_fin: str = Form(...),
    resumen: str = Form(None),
    descripcion: str = Form(None),
    db: Session = Depends(get_db)
):
    bloque = db.query(BloqueProgramacionTutorias).filter(BloqueProgramacionTutorias.id == bloque_id).first()
    
    if bloque:
        bloque.id_carrera = carrera_id
        bloque.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        bloque.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        bloque.resumen = resumen
        bloque.descripcion = descripcion
        db.commit()
        
        return RedirectResponse(
             url=f"/admin/tutorias/programar/{bloque.id}/clases", 
             status_code=303
         )
    
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.get("/tutorias/programar/{bloque_id}/clases")
def ver_programar_clases(
    request: Request,
    bloque_id: int,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Bloque
    bloque = db.query(BloqueProgramacionTutorias).filter(BloqueProgramacionTutorias.id == bloque_id).first()
    if not bloque:
         # Manejo de error básico
         return RedirectResponse(url="/admin/dashboard", status_code=303)

    # 3. Clases (Logic simplificada: traer todas las clases del semestre actual)
    # En un caso real filtrariamos por la carrera del bloque
    from ...services.clase import ClaseService
    # Traemos clases del semestre del bloque
    clases = ClaseService.get_dashboard_clases(db, semestre_id=bloque.id_semestre, carrera_id=bloque.id_carrera)
    
    return templates.TemplateResponse(
        "admin/programar_clases.html",
        {
            "request": request,
            "user": usuario,
            "bloque": bloque,
            "clases": clases,
            "active_page": "programar"
        }
    )

@router.post("/tutorias/programar/{bloque_id}/guardar")
async def guardar_programacion_clases(
    request: Request,
    bloque_id: int,
    db: Session = Depends(get_db)
):
    # 1. Obtener datos del formulario
    form_data = await request.form()
    
    # 2. Iterar sobre los datos y buscar claves 'ambiente_{clase_id}'
    from ...services.clase import ClaseService

    for key, value in form_data.items():
        if key.startswith("ambiente_"):
            try:
                clase_id = int(key.split("_")[1])
                codigo_ambiente = str(value)
                
                # Usar el servicio para asignar/crear ambiente
                ClaseService.assign_ambiente_by_codigo(db, clase_id, codigo_ambiente)
                
            except ValueError:
                continue # Ignorar claves mal formadas

    # 3. Finalizar (Redirigir al dashboard o donde corresponda)
    return RedirectResponse(url="/admin/dashboard", status_code=303)

from sqlalchemy.orm import joinedload
from ...models.sesion_programada import SesionProgramada
from ...models.clase_tutoria import ClaseTutoria
from ...models.carrera import Carrera

@router.get("/tutorias/historial")
def ver_historial_tutorias(
    request: Request,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Sesiones Realizadas (Historial)
    sesiones = (
        db.query(SesionProgramada)
        .options(joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.carrera))
        .filter(SesionProgramada.estado == 'REALIZADA')
        .order_by(SesionProgramada.fecha_hora_inicio.desc())
        .all()
    )

    return templates.TemplateResponse(
        "admin/historial_tutorias.html",
        {
            "request": request,
            "user": usuario,
            "sesiones": sesiones,
            "active_page": "historial"
        }
    )

@router.get("/tutorias/programadas")
def ver_tutorias_programadas(
    request: Request,
    db: Session = Depends(get_db)
):
    # 1. Admin Mock
    usuario = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # 2. Obtener Sesiones Programadas (Futuras)
    sesiones = (
        db.query(SesionProgramada)
        .options(joinedload(SesionProgramada.clase).joinedload(ClaseTutoria.carrera))
        .filter(SesionProgramada.estado == 'PROGRAMADA')
        .order_by(SesionProgramada.fecha_hora_inicio.asc())
        .all()
    )

    return templates.TemplateResponse(
        "admin/tutorias_programadas.html",
        {
            "request": request,
            "user": usuario,
            "sesiones": sesiones,
            "active_page": "tutorias" 
        }
    )
