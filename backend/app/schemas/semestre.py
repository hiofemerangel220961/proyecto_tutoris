from pydantic import BaseModel
from typing import Optional
from datetime import date

class SemestreBase(BaseModel):
    codigo: str
    anio: int
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    activo: bool = False
    estado_actual: str = "PLANEADO"

class SemestreCreate(SemestreBase):
    pass

class SemestreUpdate(BaseModel):
    codigo: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[bool] = None
    estado_actual: Optional[str] = None

class SemestreRead(SemestreBase):
    id: int

    class Config:
        from_attributes = True