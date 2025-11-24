from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from ..models.semestre import Semestre
from ..schemas.semestre import SemestreCreate, SemestreRead

class SemestreService:

    @staticmethod
    def get_all(db: Session) -> List[Semestre]:
        """Devuelve todos los semestres ordenados por año y periodo."""
        return db.query(Semestre).order_by(Semestre.anio.desc(), Semestre.periodo.desc()).all()

    @staticmethod
    def create(db: Session, data: SemestreCreate) -> Semestre:
        """Crea un nuevo semestre."""
        # 1. Verificar si ya existe ese código (ej. 2025-I)
        existe = db.query(Semestre).filter(Semestre.codigo == data.codigo).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El semestre {data.codigo} ya existe."
            )

        # 2. Crear el objeto
        # Por defecto nace en estado PLANEADO (activo=False)
        nuevo = Semestre(
            codigo=data.codigo,
            anio=data.anio,
            periodo=data.periodo,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            activo=False,
            estado_actual="PLANEADO"
        )
        
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo