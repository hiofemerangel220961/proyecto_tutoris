from sqlalchemy import Column, Integer, String, Boolean
from ..db.database import Base

class Ambiente(Base):
    __tablename__ = "Ambiente"

    id = Column("id_ambiente", Integer, primary_key=True, index=True)
    nombre = Column("nombre_ambiente", String, nullable=False) # Agregado para nombre amigable
    codigo = Column("codigo_ambiente", String, nullable=False)
    tipo = Column(String, default="AULA") # AULA, OFICINA
    capacidad = Column(Integer, nullable=True)
    ubicacion = Column(String, nullable=True)
    activo = Column("estado_activo", Boolean, default=True)