from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .db.database import Base, engine, SessionLocal
from .models import rol, usuario
from .models.rol import Rol
from .models.usuario import Usuario
# Modelos adicionales para que SQLAlchemy los reconozca en create_all
from .models.carrera import Carrera
from .models.semestre import Semestre
from .models.ambiente import Ambiente
from .models.tutor import Tutor
from .models.estudiante import Estudiante
from .models.clase_tutoria import ClaseTutoria
from .models.asignacion_tutorado import AsignacionTutorado
from .models.bloque_programacion_tutorias import BloqueProgramacionTutorias
from .models.sesion_programada import SesionProgramada
from .models.sesion_tutoria import SesionTutoria
from .models.detalle_tutoria import DetalleTutoria
from .models.documento_adjunto import DocumentoAdjunto
from .models.notificacion import Notificacion
from .models.solicitud_cuenta import SolicitudCuenta

from .core.security import hash_password

# Importamos los routers
from .api.auth import routes as auth_router
from .api.admin import routes as admin_router
from .api.admin import clases as admin_clases_router # <-- NUEVA RUTA
from .api.tutor import routes as tutor_router
from .api.verificador import routes as verificador_router
#anadido
from .api.admin import tutorias as admin_tutorias_router
from .api.admin import usuarios as admin_usuarios_router
#---------
# Configuración de directorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Crear tablas en BD (si no existen)
Base.metadata.create_all(bind=engine)

def init_data():
    """
    Función que se ejecuta al iniciar la app.
    Crea los roles básicos y el usuario ADMINISTRADOR por defecto.
    """
    db = SessionLocal()
    try:
        # 1. Crear Roles si no existen
        roles_base = ["ADMINISTRADOR", "TUTOR", "VERIFICADOR"]
        for nombre in roles_base:
            existe = db.query(Rol).filter(Rol.nombre_rol == nombre).first()
            if not existe:
                db.add(Rol(nombre_rol=nombre, descripcion=f"Rol {nombre.lower()}"))
        db.commit()

        # 2. Crear usuario ADMIN por defecto
        admin_email = "admin@tutorias.com"
        admin = db.query(Usuario).filter(Usuario.correo == admin_email).first()
        
        if not admin:
            # Buscamos el ID del rol de administrador
            rol_admin = db.query(Rol).filter(Rol.nombre_rol == "ADMINISTRADOR").first()
            
            # CAMBIOS AQUÍ 👇
            nuevo_admin = Usuario(
                nombres="Tulio",           # Antes: Admin
                apellidos="Tribiño",       # Antes: Principal
                correo=admin_email,
                telefono="999999999",
                contrasena_hash=hash_password("admin123"),
                id_rol=rol_admin.id_rol,
                estado="ACTIVO",
                foto_perfil_url=None,      # Por defecto sin foto
            )
            db.add(nuevo_admin)
            db.commit()
            print(f"✅ Usuario Admin creado: {admin_email} (Tulio Tribiño)")
        else:
            # Opcional: Si ya existe, podrías querer actualizarle el nombre si es el viejo
            # pero lo más rápido es borrar el archivo tutorias.db para que se regenere,
            # o simplemente dejarlo así.
            print("ℹ️ El usuario Admin ya existe.")
            
    except Exception as e:
        print(f"❌ Error inicializando datos: {e}")
        db.rollback()
    finally:
        db.close()

# Ejecutar inicialización de datos
init_data()

app = FastAPI(title="Sistema de Tutorías")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# --- REGISTRO DE RUTAS ---

# 1. Rutas de Autenticación (Login, Register, etc.)
app.include_router(auth_router.router, tags=["auth"])

# 2. Rutas de Admin
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(admin_tutorias_router.router, tags=["admin-tutorias"])
app.include_router(admin_clases_router.router, prefix="/admin", tags=["admin-clases"])
app.include_router(admin_usuarios_router.router, prefix="/admin", tags=["admin-usuarios"])


# 3. Rutas de Tutor
app.include_router(tutor_router.router, prefix="/tutor", tags=["tutor"])

# 4. Rutas de Verificador
app.include_router(verificador_router.router, prefix="/verificador", tags=["verificador"])




@app.get("/")
def root():
    return {"message": "API del Sistema de Tutorías funcionando. Ve a /login para entrar."}

@app.get("/health")
def health_check():
    return {"status": "ok"}