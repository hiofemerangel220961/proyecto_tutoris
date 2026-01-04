from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SesionProgramadaBase(BaseModel):
    tipo_sesion: Optional[str] = None
    fecha_hora_inicio: datetime
    fecha_hora_fin: Optional[datetime] = None
    resumen: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = "PROGRAMADA"

class SesionProgramadaCreate(SesionProgramadaBase):
    id_bloque: Optional[int] = None
    id_clase: Optional[int] = None
    id_tutor: Optional[int] = None
    id_ambiente: Optional[int] = None

class SesionProgramadaUpdate(BaseModel):
    tipo_sesion: Optional[str] = None
    fecha_hora_inicio: Optional[datetime] = None
    fecha_hora_fin: Optional[datetime] = None
    resumen: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    id_ambiente: Optional[int] = None

class SesionProgramadaRead(SesionProgramadaBase):
    id: int
    id_bloque: Optional[int] = None
    id_clase: Optional[int] = None
    id_tutor: Optional[int] = None
    id_ambiente: Optional[int] = None

    class Config:
        from_attributes = True
