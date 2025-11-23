from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class AsignacionTutorado(Base):
    __tablename__ = "AsignacionTutorado"

    id = Column("id_asignacion", Integer, primary_key=True, index=True)
    id_clase = Column(Integer, ForeignKey("Clase.id_clase"), nullable=False)
    id_estudiante = Column(Integer, ForeignKey("Estudiante.id_estudiante"), nullable=False)
    
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="VIGENTE") # VIGENTE, RETIRADO

    clase = relationship("ClaseTutoria", back_populates="asignaciones")
    estudiante = relationship("Estudiante", back_populates="asignaciones")