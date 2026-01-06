from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload
from pathlib import Path

from ...db.deps import get_db
from ...models.usuario import Usuario
from ...models.rol import Rol
from ...models.solicitud_cuenta import SolicitudCuenta
from ...models.tutor import Tutor
from ...models.carrera import Carrera
from ...core.security import hash_password

router = APIRouter(tags=["admin-usuarios"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Map URL type to Role names
ROLE_MAP = {
    "administradores": "ADMINISTRADOR",
    "tutores": "TUTOR",
    "verificadores": "VERIFICADOR"
}

@router.get("/usuarios/{tipo}")
def ver_usuarios(
    request: Request,
    tipo: str,
    db: Session = Depends(get_db)
):
    usuario_admin = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()

    # Case 1: Solicitudes
    if tipo == "solicitudes":
        solicitudes = db.query(SolicitudCuenta).filter(SolicitudCuenta.estado == "PENDIENTE").all()
        return templates.TemplateResponse(
            "admin/gestion_usuarios.html",
            {
                "request": request,
                "user": usuario_admin,
                "items": solicitudes,
                "active_tab": tipo,
                "active_page": "usuarios"
            }
        )

    # Case 2: Users by Role
    if tipo in ROLE_MAP:
        rol_nombre = ROLE_MAP[tipo]
        usuarios = (
            db.query(Usuario)
            .join(Rol)
            .filter(Rol.nombre_rol == rol_nombre)
            .filter(Usuario.estado != "ELIMINADO") # Assume soft delete or just filter
            .all()
        )
        return templates.TemplateResponse(
            "admin/gestion_usuarios.html",
            {
                "request": request,
                "user": usuario_admin,
                "items": usuarios,
                "active_tab": tipo,
                "active_page": "usuarios"
            }
        )
    
    # Fallback
    return RedirectResponse("/admin/dashboard")

# --- Actions ---

@router.post("/usuarios/{usuario_id}/activar")
def activar_usuario(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if user:
        user.estado = "ACTIVO"
        db.commit()
    # Redirect back to referer or default
    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/admin/usuarios/administradores", status_code=303)

@router.post("/usuarios/{usuario_id}/desactivar")
def desactivar_usuario(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if user:
        user.estado = "INACTIVO"
        db.commit()
    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/admin/usuarios/administradores", status_code=303)

@router.post("/usuarios/{usuario_id}/eliminar")
def eliminar_usuario(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if user:
        # Hard delete or Soft delete? Design implies soft or hard. Let's do hard mainly for seed data mgmt, or soft if preferred.
        # User requested "Delete".
        db.delete(user)
        db.commit()
    referer = request.headers.get("referer")
    return RedirectResponse(referer or "/admin/usuarios/administradores", status_code=303)

@router.post("/solicitudes/{solicitud_id}/aceptar")
def aceptar_solicitud(solicitud_id: int, request: Request, db: Session = Depends(get_db)):
    sol = db.query(SolicitudCuenta).filter(SolicitudCuenta.id_solicitud == solicitud_id).first()
    if sol:
        # Create User
        # Find Role
        rol = db.query(Rol).filter(Rol.nombre_rol == sol.rol_solicitado).first()
        if rol:
            new_user = Usuario(
                nombres=sol.nombres,
                apellidos=sol.apellidos,
                correo=sol.correo,
                # Default password or logic to send email. For demo: 123456
                contrasena_hash=hash_password("123456"), 
                id_rol=rol.id_rol,
                telefono="000000000",
                dni="00000000",
                estado="ACTIVO"
            )
            db.add(new_user)
            db.flush() # Para obtener el id_usuario

            # Si el rol es TUTOR, creamos el registro en la tabla Tutor
            if rol.nombre_rol == "TUTOR":
                # Buscamos una carrera por defecto para el tutor (ej: la primera)
                carrera = db.query(Carrera).first()
                new_tutor = Tutor(
                    id_usuario=new_user.id_usuario,
                    id_carrera=carrera.id if carrera else 1, # Fallback a 1 si no hay carreras
                    codigo_docente="DOC001", # Placeholder
                    oficina="Pendiente",
                    activo=True
                )
                db.add(new_tutor)

            # Si el rol es ESTUDIANTE, creamos el registro en la tabla Estudiante
            if rol.nombre_rol == "ESTUDIANTE":
                # Buscamos una carrera por defecto para el estudiante
                carrera = db.query(Carrera).first()
                new_est = Estudiante(
                    id_usuario=new_user.id_usuario,
                    codigo=f"COD{new_user.id_usuario:05d}", # Generar código temporal
                    dni="00000000",
                    nombres=new_user.nombres,
                    apellidos=new_user.apellidos,
                    correo=new_user.correo,
                    telefono="000000000",
                    id_carrera=carrera.id if carrera else 1,
                    estado_academico="REGULAR"
                )
                db.add(new_est)

            # Remove request or mark approved
            db.delete(sol) 
            db.commit()
            
    return RedirectResponse("/admin/usuarios/solicitudes", status_code=303)

@router.post("/solicitudes/{solicitud_id}/rechazar")
def rechazar_solicitud(solicitud_id: int, request: Request, db: Session = Depends(get_db)):
    sol = db.query(SolicitudCuenta).filter(SolicitudCuenta.id_solicitud == solicitud_id).first()
    if sol:
        db.delete(sol)
        db.commit()
    return RedirectResponse("/admin/usuarios/solicitudes", status_code=303)
