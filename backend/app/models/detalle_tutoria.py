from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base

class DetalleTutoria(Base):
    __tablename__ = "DetalleTutoria"

    id = Column("id_detalle_tutoria", Integer, primary_key=True, index=True)
    id_sesion_tutoria = Column(Integer, ForeignKey("SesionTutoria.id_sesion_tutoria"), nullable=False, unique=True)
    
    documento_url = Column(String, nullable=True)
    detalle_academico = Column(Text, nullable=True)
    detalle_personal = Column(Text, nullable=True)
    detalle_profesional = Column(Text, nullable=True)
    
    observaciones_academico = Column(Text, nullable=True)
    observaciones_personal = Column(Text, nullable=True)
    observaciones_profesional = Column(Text, nullable=True)
    
    derivado_psicologia = Column(Boolean, default=False)
    
    # Relaciones
    sesion_tutoria = relationship("SesionTutoria", back_populates="detalle")
