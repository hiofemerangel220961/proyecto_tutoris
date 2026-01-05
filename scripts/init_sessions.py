import sys
import os
import random
from datetime import datetime, timedelta

# Add backend directory to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.clase_tutoria import ClaseTutoria
from app.models.asignacion_tutorado import AsignacionTutorado
from app.models.sesion_programada import SesionProgramada
from app.models.sesion_tutoria import SesionTutoria
from app.models.bloque_programacion_tutorias import BloqueProgramacionTutorias
from app.models.ambiente import Ambiente

def init_sessions():
    db = SessionLocal()
    try:
        print("Iniciando inicialización de sesiones...")
        
        # 1. Obtener todas las clases
        clases = db.query(ClaseTutoria).all()
        if not clases:
            print("No hay clases registradas. Ejecuta seed_data.py primero.")
            return

        ambiente = db.query(Ambiente).first()
        
        for clase in clases:
            print(f"Procesando clase: {clase.nombre} (ID: {clase.id})")
            
            # Obtener estudiantes de la clase
            asignaciones = db.query(AsignacionTutorado).filter_by(id_clase=clase.id).all()
            if not asignaciones:
                print("  -> Clase sin estudiantes asignados.")
                continue
                
            estudiantes = [a.estudiante for a in asignaciones]
            
            # Obtener o crear bloque (asumimos existe uno del seed, sino creamos dummy)
            bloque = db.query(BloqueProgramacionTutorias).first()
            
            # --- CREAR SESIONES PASADAS (REALIZADAS) ---
            # Vamos a crear ~5 sesiones pasadas
            fecha_base = datetime.utcnow() - timedelta(days=60)
            
            for i in range(5):
                fecha_sesion = fecha_base + timedelta(days=i*7) # Una por semana
                
                # Crear SesionProgramada
                sesion_prog = SesionProgramada(
                    id_bloque=bloque.id if bloque else None,
                    id_clase=clase.id,
                    id_tutor=clase.id_tutor,
                    id_ambiente=ambiente.id if ambiente else None,
                    tipo_sesion="Grupal",
                    fecha_hora_inicio=fecha_sesion,
                    fecha_hora_fin=fecha_sesion + timedelta(hours=2),
                    resumen=f"Sesión Grupal {i+1} - Seguimiento",
                    descripcion="Sesión regular de control de avance académico.",
                    estado="REALIZADA"
                )
                db.add(sesion_prog)
                db.flush() # Para tener ID
                
                # Crear SesionTutoria para cada estudiante (Asistencias)
                for est in estudiantes:
                    # Randomize attendance a bit (90% attendance)
                    if random.random() > 0.1:
                        sesion_tut = SesionTutoria(
                            id_sesion_programada=sesion_prog.id,
                            id_tutor=clase.id_tutor,
                            id_estudiante=est.id, # IMPORTANTE: ESTO FALTABA EN LA LOGICA ANTERIOR
                            tipo_tutoria="Grupal",
                            fecha_hora_realizacion=fecha_sesion,
                            estado="REALIZADA"
                        )
                        db.add(sesion_tut)
            
            # --- CREAR SESIONES FUTURAS (PROGRAMADAS) ---
            # Vamos a crear ~3 sesiones futuras
            fecha_futura_base = datetime.utcnow() + timedelta(days=2)
            for i in range(3):
                fecha_sesion = fecha_futura_base + timedelta(days=i*14)
                 
                sesion_prog = SesionProgramada(
                    id_bloque=bloque.id if bloque else None,
                    id_clase=clase.id,
                    id_tutor=clase.id_tutor,
                    id_ambiente=ambiente.id if ambiente else None,
                    tipo_sesion="Grupal",
                    fecha_hora_inicio=fecha_sesion,
                    fecha_hora_fin=fecha_sesion + timedelta(hours=2),
                    resumen=f"Sesión Programada {i+1} - Cierre",
                    descripcion="Sesión de cierre de unidad.",
                    estado="PROGRAMADA"
                )
                db.add(sesion_prog)
            
            db.commit()
            print(f"  -> Generadas 5 sesiones pasadas y 3 futuras para {len(estudiantes)} estudiantes.")
            
        print("Inicialización completada con éxito.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_sessions()
