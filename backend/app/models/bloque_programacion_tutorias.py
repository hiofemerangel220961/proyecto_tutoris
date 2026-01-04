from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class BloqueProgramacionTutorias(Base):
    __tablename__ = "BloqueProgramacionTutorias"

    id = Column("id_bloque", Integer, primary_key=True, index=True)
    id_carrera = Column(Integer, ForeignKey("Carrera.id_carrera"), nullable=True)
    id_semestre = Column(Integer, ForeignKey("Semestre.id_semestre"), nullable=True)
    
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    resumen = Column(String, nullable=True)
    descripcion = Column(String, nullable=True)
    estado = Column(String, default="ACTIVO")
    
    creado_por = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    carrera = relationship("Carrera")
    semestre = relationship("Semestre")
    creador = relationship("Usuario")
    # relacion con sesiones programadas
    sesiones_programadas = relationship("SesionProgramada", back_populates="bloque")
