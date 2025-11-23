from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base

class ClaseTutoria(Base):
    __tablename__ = "Clase"  # Nombre en BD según tu DBML

    id = Column("id_clase", Integer, primary_key=True, index=True)
    nombre = Column("nombre_clase", String, nullable=False) # Ej: "Tutoría I - Ing. Sistemas"
    
    id_tutor = Column(Integer, ForeignKey("Tutor.id_tutor"), nullable=False)
    id_carrera = Column(Integer, ForeignKey("Carrera.id_carrera"), nullable=False)
    id_semestre = Column(Integer, ForeignKey("Semestre.id_semestre"), nullable=False)
    id_ambiente = Column(Integer, ForeignKey("Ambiente.id_ambiente"), nullable=True)
    
    activo = Column("estado_activo", Boolean, default=True)

    # Relaciones
    tutor = relationship("Tutor", back_populates="clases")
    carrera = relationship("Carrera")
    semestre = relationship("Semestre", back_populates="clases")
    ambiente = relationship("Ambiente")
    
    # Lista de asignaciones (estudiantes en esta clase)
    asignaciones = relationship("AsignacionTutorado", back_populates="clase")