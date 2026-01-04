from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SesionTutoriaBase(BaseModel):
    tipo_tutoria: Optional[str] = None
    fecha_hora_realizacion: Optional[datetime] = None
    estado: Optional[str] = "REALIZADA"
    asistencia: bool = False
    riesgo_academico: bool = False

class SesionTutoriaCreate(SesionTutoriaBase):
    id_sesion_programada: Optional[int] = None
    id_tutor: Optional[int] = None
    id_estudiante: Optional[int] = None

class SesionTutoriaUpdate(BaseModel):
    estado: Optional[str] = None
    asistencia: Optional[bool] = None
    riesgo_academico: Optional[bool] = None
    fecha_hora_realizacion: Optional[datetime] = None

class SesionTutoriaRead(SesionTutoriaBase):
    id: int
    id_sesion_programada: Optional[int] = None
    id_tutor: Optional[int] = None
    id_estudiante: Optional[int] = None

    class Config:
        from_attributes = True
