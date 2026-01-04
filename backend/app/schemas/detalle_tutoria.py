from pydantic import BaseModel
from typing import Optional

class DetalleTutoriaBase(BaseModel):
    dimension_personal: Optional[str] = None
    dimension_profesional: Optional[str] = None
    dimension_academica: Optional[str] = None
    observaciones: Optional[str] = None
    detalle_academico: Optional[str] = None
    observaciones_academico: Optional[str] = None
    derivado_psicologia: bool = False
    derivado_otra_area: bool = False

class DetalleTutoriaCreate(DetalleTutoriaBase):
    id_sesion_tutoria: int

class DetalleTutoriaUpdate(BaseModel):
    dimension_personal: Optional[str] = None
    dimension_profesional: Optional[str] = None
    dimension_academica: Optional[str] = None
    observaciones: Optional[str] = None
    detalle_academico: Optional[str] = None
    observaciones_academico: Optional[str] = None
    derivado_psicologia: Optional[bool] = None
    derivado_otra_area: Optional[bool] = None

class DetalleTutoriaRead(DetalleTutoriaBase):
    id: int
    id_sesion_tutoria: int

    class Config:
        from_attributes = True
