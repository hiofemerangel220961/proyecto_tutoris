from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class Notificacion(Base):
    __tablename__ = "Notificacion"

    id = Column("id_notificacion", Integer, primary_key=True, index=True)
    id_usuario_destino = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False)
    
    titulo = Column(String, nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String, nullable=True) # INFO, WARNING, ALERTA
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    leida = Column(Boolean, default=False)
    
    # Relaciones
    usuario = relationship("Usuario")
