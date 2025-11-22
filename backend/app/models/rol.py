from sqlalchemy import Column, Integer, String
from backend.app.db.database import Base

class Rol(Base):
    __tablename__ = "Rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)