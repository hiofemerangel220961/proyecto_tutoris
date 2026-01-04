from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BloqueProgramacionBase(BaseModel):
    id_carrera: Optional[int] = None
    id_semestre: Optional[int] = None
    fecha_inicio: date
    fecha_fin: date
    resumen: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = "ACTIVO"

class BloqueProgramacionCreate(BloqueProgramacionBase):
    pass

class BloqueProgramacionUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    resumen: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None

class BloqueProgramacionRead(BloqueProgramacionBase):
    id: int
    creado_por: Optional[int] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True
