from fastapi import FastAPI

from .db.database import Base, engine, SessionLocal
from .models import rol, usuario  # registra modelos
from .models.rol import Rol
from .models.usuario import Usuario
from .core.security import hash_password
from .api import auth as auth_router


# Crear todas las tablas en la BD
Base.metadata.create_all(bind=engine)


def init_data():
    """Crea roles básicos y un admin por defecto, si no existen."""
    db = SessionLocal()
    try:
        # Crear roles si no existen
        roles_base = ["ADMINISTRADOR", "TUTOR", "VERIFICADOR"]
        for nombre in roles_base:
            existe = db.query(Rol).filter(Rol.nombre_rol == nombre).first()
            if not existe:
                nuevo_rol = Rol(nombre_rol=nombre, descripcion=f"Rol {nombre.lower()}")
                db.add(nuevo_rol)
        db.commit()

        # Crear admin por defecto
        admin_email = "admin@tutorias.com"
        admin = db.query(Usuario).filter(Usuario.correo == admin_email).first()
        if not admin:
            rol_admin = db.query(Rol).filter(Rol.nombre_rol == "ADMINISTRADOR").first()
            admin = Usuario(
                nombres="Admin",
                apellidos="Principal",
                correo=admin_email,
                telefono=0,
                contrasena_hash=hash_password("admin123"),
                id_rol=rol_admin.id_rol,
                estado="ACTIVO",
                foto_perfil_url=None,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


# Inicializar datos al arrancar la app
init_data()

app = FastAPI(title="Sistema de Tutorías")

# Registrar router de autenticación
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "API del Sistema de Tutorías funcionando"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
