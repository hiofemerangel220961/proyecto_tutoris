from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentoAdjuntoBase(BaseModel):
    tipo_documento: Optional[str] = None
    nombre_archivo: str
    ruta_archivo: str
    descripcion: Optional[str] = None

class DocumentoAdjuntoCreate(DocumentoAdjuntoBase):
    id_estudiante: Optional[int] = None
    id_sesion_tutoria: Optional[int] = None
    subido_por: Optional[int] = None

class DocumentoAdjuntoRead(DocumentoAdjuntoBase):
    id: int
    id_estudiante: Optional[int] = None
    id_sesion_tutoria: Optional[int] = None
    subido_por: Optional[int] = None
    fecha_subida: datetime

    class Config:
        from_attributes = True
