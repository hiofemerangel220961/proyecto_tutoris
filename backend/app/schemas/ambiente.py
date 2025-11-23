from pydantic import BaseModel
from typing import Optional

class AmbienteBase(BaseModel):
    nombre: str
    codigo: str
    tipo: str = "AULA"
    capacidad: Optional[int] = None
    ubicacion: Optional[str] = None
    activo: bool = True

class AmbienteCreate(AmbienteBase):
    pass

class AmbienteUpdate(BaseModel):
    nombre: Optional[str] = None
    capacidad: Optional[int] = None
    activo: Optional[bool] = None

class AmbienteRead(AmbienteBase):
    id: int

    class Config:
        from_attributes = True