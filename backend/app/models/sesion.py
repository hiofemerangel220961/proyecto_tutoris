from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class Sesion(Base):
    __tablename__ = "Sesion"

    id = Column("id_sesion", Integer, primary_key=True, index=True)
    id_clase = Column(Integer, ForeignKey("Clase.id_clase"), nullable=False)
    id_ambiente = Column(Integer, ForeignKey("Ambiente.id_ambiente"), nullable=True)
    
    fecha = Column(DateTime, nullable=False)
    tema = Column(String, nullable=True)
    estado = Column(String, default="PROGRAMADA") # PROGRAMADA, REALIZADA, CANCELADA
    
    # Relaciones
    clase = relationship("ClaseTutoria", back_populates="sesiones")
    ambiente = relationship("Ambiente")
