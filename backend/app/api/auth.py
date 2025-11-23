from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.deps import get_db
from ..models.usuario import Usuario
from ..models.solicitud_cuenta import SolicitudCuenta
from ..models.recuperacion_password import RecuperacionPassword
from ..core.security import verify_password, hash_password
from ..schemas.auth import (
    LoginRequest,
    LoginResponse,
    UsuarioBase,
    RegisterRequest,
    RegisterResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario_db: Usuario | None = (
        db.query(Usuario).filter(Usuario.correo == data.correo).first()
    )

    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if usuario_db.estado != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no activo",
        )

    if not verify_password(data.contrasena, usuario_db.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    usuario_out = UsuarioBase(
        id_usuario=usuario_db.id_usuario,
        nombres=usuario_db.nombres,
        apellidos=usuario_db.apellidos,
        correo=usuario_db.correo,
        estado=usuario_db.estado,
        rol=usuario_db.rol.nombre_rol,
    )

    return LoginResponse(usuario=usuario_out)


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # 1. Verificar si ya existe usuario con ese correo
    usuario_existente = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese correo",
        )

    # 2. Verificar si ya hay una solicitud pendiente con ese correo
    solicitud_pendiente = (
        db.query(SolicitudCuenta)
        .filter(
            SolicitudCuenta.correo == data.correo,
            SolicitudCuenta.estado == "PENDIENTE",
        )
        .first()
    )

    if solicitud_pendiente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una solicitud pendiente con ese correo",
        )

    # 3. Crear nueva solicitud
    nueva = SolicitudCuenta(
        nombres=data.nombres,
        apellidos=data.apellidos,
        correo=data.correo,
        rol_solicitado=data.rol_solicitado,
        estado="PENDIENTE",
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return RegisterResponse(
        id_solicitud=nueva.id_solicitud,
        estado=nueva.estado,
        mensaje="Solicitud de cuenta creada. Un administrador deberá aprobarla.",
    )

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Buscar usuario por correo
    usuario_db: Usuario | None = (
        db.query(Usuario).filter(Usuario.correo == data.correo).first()
    )

    # Por seguridad, aunque no exista el usuario, devolvemos el mismo mensaje
    if not usuario_db:
        return ForgotPasswordResponse(
            mensaje="Si el correo existe, se enviará un enlace para cambiar la contraseña."
        )

    # Crear token de recuperación
    token = secrets.token_urlsafe(32)
    ahora = datetime.utcnow()
    expira = ahora + timedelta(hours=1)

    rec = RecuperacionPassword(
        id_usuario=usuario_db.id_usuario,
        token=token,
        fecha_creacion=ahora,
        fecha_expiracion=expira,
        usado=False,
    )
    db.add(rec)
    db.commit()

    # Aquí en un futuro se enviará el email con un enlace tipo:
    # http://tuservidor/reset-password?token=XYZ
    # Por ahora solo devolvemos mensaje genérico.
    return ForgotPasswordResponse(
        mensaje="Solicitud enviada. Revise su correo electrónico para continuar."
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Buscar token
    rec: RecuperacionPassword | None = (
        db.query(RecuperacionPassword)
        .filter(RecuperacionPassword.token == data.token)
        .first()
    )

    if not rec or rec.usado or rec.fecha_expiracion < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enlace de recuperación inválido o expirado.",
        )

    usuario_db = db.query(Usuario).filter(Usuario.id_usuario == rec.id_usuario).first()
    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado.",
        )

    # Actualizar la contraseña
    usuario_db.contrasena_hash = hash_password(data.nueva_contrasena)
    rec.usado = True

    db.commit()

    return ResetPasswordResponse(
        mensaje="La contraseña se ha actualizado correctamente. Ahora puede iniciar sesión."
    )
