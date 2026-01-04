import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

from backend.app.db.database import SessionLocal
from backend.app.models.rol import Rol
from backend.app.models.usuario import Usuario

def reactivate_admin():
    db = SessionLocal()
    try:
        user = db.query(Usuario).filter(Usuario.correo == "admin@tutorias.com").first()
        if user:
            print(f"User found: {user.correo}, State: {user.estado}")
            user.estado = "ACTIVO"
            db.commit()
            print(f"User {user.correo} has been reactivated successfully.")
        else:
            print("User admin@tutorias.com not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reactivate_admin()
