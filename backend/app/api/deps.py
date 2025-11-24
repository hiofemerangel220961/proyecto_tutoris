from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.usuario import Usuario


def get_current_user():
    # Aquí debes colocar tu extracción real del usuario desde cookie/token.
    # Por ahora dejo un mock para que pruebes:
    return Usuario(id_usuario=1, nombres="Admin", apellidos="Principal", id_rol=1)


def get_current_admin_user(
    user: Usuario = Depends(get_current_user),
):
    if user.id_rol != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no autorizado",
        )
    return user
