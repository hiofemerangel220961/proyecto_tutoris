from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base

class Estudiante(Base):
    __tablename__ = "Estudiante"

    id = Column("id_estudiante", Integer, primary_key=True, index=True)
    # Relación opcional con usuario (login)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=True, unique=True)
    
    codigo = Column("codigo_estudiante", String, unique=True, nullable=False)
    dni = Column("dni_estudiante", String, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    
    id_carrera = Column(Integer, ForeignKey("Carrera.id_carrera"), nullable=False)
    
    estado_academico = Column(String, default="REGULAR") # REGULAR, RETIRADO, EGRESADO

    # Relaciones
    usuario = relationship("Usuario")
    carrera = relationship("Carrera", back_populates="estudiantes")
    asignaciones = relationship("AsignacionTutorado", back_populates="estudiante")