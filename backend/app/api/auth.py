from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.deps import get_db
from ..models.usuario import Usuario
from ..core.security import verify_password
from ..schemas.auth import LoginRequest, LoginResponse, UsuarioBase

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por correo
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

    # Verificar contraseña
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
