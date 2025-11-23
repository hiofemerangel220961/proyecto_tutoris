from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base

class Carrera(Base):
    __tablename__ = "Carrera"

    id = Column("id_carrera", Integer, primary_key=True, index=True)
    nombre = Column("nombre_carrera", String, nullable=False)
    codigo = Column("codigo_carrera", String, nullable=False)
    facultad = Column(String, nullable=True)
    activo = Column("estado", Boolean, default=True) # Mapeamos 'estado' del DBML a booleano para facilitar lógica

    # Relaciones (se llenarán automáticamente cuando definamos los otros modelos)
    estudiantes = relationship("Estudiante", back_populates="carrera")
    tutores = relationship("Tutor", back_populates="carrera")