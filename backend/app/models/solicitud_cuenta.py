from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from ..db.database import Base


class SolicitudCuenta(Base):
    __tablename__ = "SolicitudCuenta"

    id_solicitud = Column(Integer, primary_key=True, index=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    rol_solicitado = Column(String, nullable=False)  # ADMINISTRADOR, TUTOR, VERIFICADOR
    estado = Column(String, default="PENDIENTE")     # PENDIENTE, APROBADA, RECHAZADA
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    id_admin_resuelve = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=True)
