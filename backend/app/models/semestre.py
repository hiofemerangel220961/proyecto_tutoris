from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base

class Semestre(Base):
    __tablename__ = "Semestre"

    id = Column("id_semestre", Integer, primary_key=True, index=True)
    codigo = Column("codigo_semestre", String, nullable=False) # Ej: 2025-I
    anio = Column(Integer, nullable=False)
    periodo = Column(String, nullable=False) # I, II, VERANO
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    # estado: PLANEADO, ACTIVO, CERRADO. 
    # Usamos un booleano 'activo' para consultas rápidas, o string 'estado_actual'
    activo = Column(Boolean, default=False) 
    estado_actual = Column("estado", String, default="PLANEADO")

    clases = relationship("ClaseTutoria", back_populates="semestre")