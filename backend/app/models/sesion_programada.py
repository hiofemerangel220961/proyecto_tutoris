from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from ..db.database import Base

class SesionProgramada(Base):
    __tablename__ = "SesionProgramada"

    id = Column("id_sesion_programada", Integer, primary_key=True, index=True)
    id_bloque = Column(Integer, ForeignKey("BloqueProgramacionTutorias.id_bloque"), nullable=True)
    id_clase = Column(Integer, ForeignKey("Clase.id_clase"), nullable=True)
    id_tutor = Column(Integer, ForeignKey("Tutor.id_tutor"), nullable=True)
    id_ambiente = Column(Integer, ForeignKey("Ambiente.id_ambiente"), nullable=True)
    
    tipo_sesion = Column(String, nullable=True) # Individual / Grupal
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=True)
    
    resumen = Column(String, nullable=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(String, default="PROGRAMADA") # PROGRAMADA, REALIZADA, CANCELADA
    
    # Relaciones
    bloque = relationship("BloqueProgramacionTutorias", back_populates="sesiones_programadas")
    clase = relationship("ClaseTutoria", back_populates="sesiones_programadas")
    tutor = relationship("Tutor")
    ambiente = relationship("Ambiente")
    
    # Relacion con la ejecucion (SesionTutoria)
    sesiones_realizadas = relationship("SesionTutoria", back_populates="sesion_programada")
