from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import Base


class Usuario(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    dni = Column(String, nullable=True) # Added to match diagram
    correo = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)  # string para evitar líos
    contrasena_hash = Column(String, nullable=False)
    id_rol = Column(Integer, ForeignKey("Rol.id_rol"), nullable=False)
    estado = Column(String, default="PENDIENTE")  # PENDIENTE, ACTIVO, BLOQUEADO
    foto_perfil_url = Column(String, nullable=True)

    # relación con Rol (se resuelve por nombre de clase)
    rol = relationship("Rol")
