from pydantic import BaseModel
from typing import Optional

# Base: datos comunes
class CarreraBase(BaseModel):
    nombre: str
    codigo: str
    facultad: Optional[str] = None
    activo: bool = True

# Create: lo que se necesita para crear (todo lo base)
class CarreraCreate(CarreraBase):
    pass

# Update: todo opcional por si solo quieres cambiar el nombre
class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    facultad: Optional[str] = None
    activo: Optional[bool] = None

# Read: Lo que devuelve la API (incluye el ID)
class CarreraRead(CarreraBase):
    id: int

    class Config:
        from_attributes = True