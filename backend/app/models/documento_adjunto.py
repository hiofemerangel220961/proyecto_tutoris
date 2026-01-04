from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class DocumentoAdjunto(Base):
    __tablename__ = "DocumentoAdjunto"

    id = Column("id_documento", Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, ForeignKey("Estudiante.id_estudiante"), nullable=True)
    id_sesion_tutoria = Column(Integer, ForeignKey("SesionTutoria.id_sesion_tutoria"), nullable=True)
    subido_por = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=True)
    
    tipo_documento = Column(String, nullable=True)
    nombre_archivo = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_subida = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    estudiante = relationship("Estudiante")
    sesion_tutoria = relationship("SesionTutoria", back_populates="documentos")
    usuario = relationship("Usuario")
