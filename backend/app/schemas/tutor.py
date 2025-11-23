from pydantic import BaseModel
from typing import Optional
from .usuario import UsuarioMinimo
from .carrera import CarreraRead

class TutorBase(BaseModel):
    codigo_docente: Optional[str] = None
    oficina: Optional[str] = None
    activo: bool = True

class TutorCreate(TutorBase):
    id_usuario: int
    id_carrera: int

class TutorRead(TutorBase):
    id: int
    usuario: Optional[UsuarioMinimo] = None
    carrera: Optional[CarreraRead] = None

    class Config:
        from_attributes = True