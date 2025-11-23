from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import Base


class RecuperacionPassword(Base):
    __tablename__ = "RecuperacionPassword"

    id_recuperacion = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_expiracion = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)

    usuario = relationship("Usuario")
