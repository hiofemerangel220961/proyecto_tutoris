from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioMinimo(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: EmailStr
    foto_perfil_url: Optional[str] = None

    class Config:
        from_attributes = True