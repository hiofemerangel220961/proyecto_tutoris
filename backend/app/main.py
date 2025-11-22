from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db.database import Base, engine, SessionLocal
from .models import rol, usuario
from .models.rol import Rol
from .models.usuario import Usuario
from .core.security import hash_password
from .api import auth as auth_router

# BASE_DIR = carpeta raíz del proyecto (proyecto_tutorias)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

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

# 👇 SOLO UNA VEZ
app = FastAPI(title="Sistema de Tutorías")

# Montar estáticos y templates usando rutas absolutas
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Registrar router API (auth)
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "API del Sistema de Tutorías funcionando"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})
