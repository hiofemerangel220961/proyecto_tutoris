from pydantic import BaseModel
from typing import Optional, List
from .tutor import TutorRead
from .carrera import CarreraRead
from .semestre import SemestreRead
from .ambiente import AmbienteRead

class ClaseBase(BaseModel):
    nombre: str
    activo: bool = True

class ClaseCreate(ClaseBase):
    id_tutor: int
    id_carrera: int
    id_semestre: int
    id_ambiente: Optional[int] = None

class ClaseUpdate(BaseModel):
    nombre: Optional[str] = None
    id_tutor: Optional[int] = None
    id_ambiente: Optional[int] = None
    activo: Optional[bool] = None

class ClaseRead(ClaseBase):
    id: int
    tutor: Optional[TutorRead] = None
    carrera: Optional[CarreraRead] = None
    semestre: Optional[SemestreRead] = None
    ambiente: Optional[AmbienteRead] = None

    class Config:
        from_attributes = True