from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str
    tipo: Optional[str] = "INFO"
    leida: bool = False

class NotificacionCreate(NotificacionBase):
    id_usuario_destino: int

class NotificacionUpdate(BaseModel):
    leida: bool

class NotificacionRead(NotificacionBase):
    id: int
    id_usuario_destino: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
