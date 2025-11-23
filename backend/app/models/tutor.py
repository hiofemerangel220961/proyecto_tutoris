from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base

class Tutor(Base):
    __tablename__ = "Tutor"

    id = Column("id_tutor", Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False, unique=True)
    id_carrera = Column(Integer, ForeignKey("Carrera.id_carrera"), nullable=False)
    
    codigo_docente = Column(String, nullable=True)
    oficina = Column(String, nullable=True)
    activo = Column("estado_activo", Boolean, default=True)

    # Relaciones
    usuario = relationship("Usuario")
    carrera = relationship("Carrera", back_populates="tutores")
    clases = relationship("ClaseTutoria", back_populates="tutor")