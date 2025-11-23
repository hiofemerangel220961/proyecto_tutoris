from pydantic import BaseModel
from typing import Optional
from .carrera import CarreraRead
from .usuario import UsuarioMinimo

class EstudianteBase(BaseModel):
    codigo: str
    dni: str
    nombres: str
    apellidos: str
    correo: Optional[str] = None
    telefono: Optional[str] = None
    estado_academico: str = "REGULAR"

class EstudianteCreate(EstudianteBase):
    id_carrera: int
    id_usuario: Optional[int] = None

class EstudianteRead(EstudianteBase):
    id: int
    carrera: Optional[CarreraRead] = None
    usuario: Optional[UsuarioMinimo] = None

    class Config:
        from_attributes = True