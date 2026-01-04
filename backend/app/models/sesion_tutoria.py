from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db.database import Base

class SesionTutoria(Base):
    __tablename__ = "SesionTutoria"

    id = Column("id_sesion_tutoria", Integer, primary_key=True, index=True)
    id_sesion_programada = Column(Integer, ForeignKey("SesionProgramada.id_sesion_programada"), nullable=False)
    id_tutor = Column(Integer, ForeignKey("Tutor.id_tutor"), nullable=False)
    id_estudiante = Column(Integer, ForeignKey("Estudiante.id_estudiante"), nullable=True) # Nullable si es grupal? El diagrama dice fk
    
    tipo_tutoria = Column(String, nullable=True)
    fecha_hora_realizacion = Column(DateTime, nullable=False)
    estado = Column(String, default="REALIZADA")
    
    # Relaciones
    sesion_programada = relationship("SesionProgramada", back_populates="sesiones_realizadas")
    tutor = relationship("Tutor")
    estudiante = relationship("Estudiante")
    
    detalle = relationship("DetalleTutoria", back_populates="sesion_tutoria", uselist=False)
    documentos = relationship("DocumentoAdjunto", back_populates="sesion_tutoria")
