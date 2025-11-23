from datetime import datetime, timedelta
import secrets

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.usuario import Usuario
from ..models.solicitud_cuenta import SolicitudCuenta
from ..models.recuperacion_password import RecuperacionPassword
from ..core.security import verify_password, hash_password
from ..schemas.auth import (
    LoginRequest, UsuarioBase,
    RegisterRequest, RegisterResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse
)

class AuthService:
    
    @staticmethod
    def authenticate_user(db: Session, data: LoginRequest):
        """Verifica credenciales y estado del usuario."""
        usuario_db = db.query(Usuario).filter(Usuario.correo == data.correo).first()

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

        # Convertimos al esquema de salida
        return UsuarioBase(
            id_usuario=usuario_db.id_usuario,
            nombres=usuario_db.nombres,
            apellidos=usuario_db.apellidos,
            correo=usuario_db.correo,
            estado=usuario_db.estado,
            rol=usuario_db.rol.nombre_rol,
        )

    @staticmethod
    def register_user_solicitude(db: Session, data: RegisterRequest):
        """Crea una solicitud de cuenta si no existe el usuario ni la solicitud."""
        # 1. Verificar usuario existente
        usuario_existente = db.query(Usuario).filter(Usuario.correo == data.correo).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese correo",
            )

        # 2. Verificar solicitud pendiente
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

        # 3. Crear solicitud
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

    @staticmethod
    def request_password_reset(db: Session, data: ForgotPasswordRequest):
        """Genera un token de recuperación si el usuario existe."""
        usuario_db = db.query(Usuario).filter(Usuario.correo == data.correo).first()
        
        # Por seguridad, no decimos si el correo existe o no, pero si existe creamos el token
        if usuario_db:
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

        return ForgotPasswordResponse(
            mensaje="Si el correo existe, se enviará un enlace para cambiar la contraseña."
        )

    @staticmethod
    def perform_reset_password(db: Session, data: ResetPasswordRequest):
        """Valida el token y actualiza la contraseña."""
        rec = (
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

        # Actualizar contraseña
        usuario_db.contrasena_hash = hash_password(data.nueva_contrasena)
        rec.usado = True
        db.commit()

        return ResetPasswordResponse(
            mensaje="La contraseña se ha actualizado correctamente. Ahora puede iniciar sesión."
        )