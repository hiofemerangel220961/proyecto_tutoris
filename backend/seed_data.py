import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.carrera import Carrera
from app.models.semestre import Semestre
from app.models.ambiente import Ambiente
from app.models.tutor import Tutor
from app.models.estudiante import Estudiante
from app.models.clase_tutoria import ClaseTutoria
from app.models.asignacion_tutorado import AsignacionTutorado
from app.models.sesion import Sesion

# Listas de datos realistas
NOMBRES = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Sofia", "Miguel", "Lucia", "Jose", "Paula", "David", "Carmen", "Jorge", "Isabel"]
APELLIDOS = ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez", "Diaz"]

def get_random_name():
    return random.choice(NOMBRES)

def get_random_lastname():
    return random.choice(APELLIDOS)

def seed_data():
    db = SessionLocal()
    try:
        print("... Iniciando poblado de datos...")

        # 1. Roles
        print("... Creando Roles")
        
        # ... (omitted lines)

        print("... Verificando Admin")
        
        # ...

        print("... Creando Semestres")

        # ...

        print("... Creando Carreras")

        # ...

        print("... Creando Ambientes")

        # ...

        print("... Creando Tutores")

        # ...

        print("... Creando Estudiantes")

        # ...

        print("... Creando Clases")

        # ...

        print("... Asignando Estudiantes y Creando Sesiones")

        # ...

        print("Datos de prueba cargados exitosamente.")

    except Exception as e:
        print(f"Error al poblar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
