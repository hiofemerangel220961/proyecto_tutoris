from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional

from ..models.clase_tutoria import ClaseTutoria
from ..models.tutor import Tutor
from ..models.usuario import Usuario
from ..models.semestre import Semestre
from ..models.asignacion_tutorado import AsignacionTutorado
from ..models.semestre import Semestre
from ..models.asignacion_tutorado import AsignacionTutorado
from ..models.sesion_programada import SesionProgramada
from ..models.ambiente import Ambiente

class ClaseService:

    @staticmethod
    def get_dashboard_clases(
        db: Session, 
        semestre_id: int, 
        search: Optional[str] = None, 
        carrera_id: Optional[int] = None
    ) -> List[ClaseTutoria]:
        """
        Obtiene las clases de un semestre específico con filtros opcionales.
        Carga relaciones (Tutor, Usuario, Carrera, Ambiente, Asignaciones) para el frontend.
        """
        # Consulta base: Clases del semestre activo
        query = db.query(ClaseTutoria).filter(ClaseTutoria.id_semestre == semestre_id)

        # Optimizamos la consulta para traer los datos relacionados de una vez
        query = query.options(
            joinedload(ClaseTutoria.tutor).joinedload(Tutor.usuario),
            joinedload(ClaseTutoria.carrera),
            joinedload(ClaseTutoria.ambiente),
            joinedload(ClaseTutoria.asignaciones) # Para contar alumnos
        )

        # Filtro 1: Búsqueda por texto (Nombre del tutor o Apellido)
        if search:
            search_term = f"%{search}%"
            query = query.join(ClaseTutoria.tutor).join(Tutor.usuario).filter(
                or_(
                    Usuario.nombres.ilike(search_term),
                    Usuario.apellidos.ilike(search_term),
                    ClaseTutoria.nombre.ilike(search_term)
                )
            )

        # Filtro 2: Por Carrera (Escuela Profesional)
        if carrera_id:
            query = query.filter(ClaseTutoria.id_carrera == carrera_id)

        return query.all()

    @staticmethod
    def get_clase_detalle(db: Session, clase_id: int) -> Optional[ClaseTutoria]:
        """
        Obtiene el detalle de una clase específica, incluyendo sesiones y estudiantes.
        """
        return db.query(ClaseTutoria).options(
            joinedload(ClaseTutoria.tutor).joinedload(Tutor.usuario),
            joinedload(ClaseTutoria.carrera),
            joinedload(ClaseTutoria.ambiente),
            joinedload(ClaseTutoria.semestre),
            joinedload(ClaseTutoria.sesiones_programadas).joinedload(SesionProgramada.ambiente),
            joinedload(ClaseTutoria.asignaciones).joinedload(AsignacionTutorado.estudiante)
        ).filter(ClaseTutoria.id == clase_id).first()

    @staticmethod
    def assign_ambiente_by_codigo(db: Session, clase_id: int, codigo: str) -> Optional[ClaseTutoria]:
        """
        Asigna un ambiente a una clase buscándolo por código. 
        Si no existe, lo crea.
        """
        clase = db.query(ClaseTutoria).filter(ClaseTutoria.id == clase_id).first()
        if not clase:
            return None

        # Normalizar código
        codigo = codigo.strip()
        if not codigo:
            return clase # No hacer nada si está vacío

        ambiente = db.query(Ambiente).filter(Ambiente.codigo == codigo).first()
        if not ambiente:
            ambiente = Ambiente(
                nombre=codigo,
                codigo=codigo,
                tipo="AULA",
                activo=True
            )
            db.add(ambiente)
            db.commit()
            db.refresh(ambiente)
        
        clase.id_ambiente = ambiente.id
        db.commit()
        db.refresh(clase)
        return clase