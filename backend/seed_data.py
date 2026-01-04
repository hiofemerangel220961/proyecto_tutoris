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
# New Models
from app.models.sesion_programada import SesionProgramada
from app.models.sesion_tutoria import SesionTutoria
from app.models.bloque_programacion_tutorias import BloqueProgramacionTutorias
from app.models.detalle_tutoria import DetalleTutoria
from app.models.documento_adjunto import DocumentoAdjunto
from app.models.notificacion import Notificacion
from app.models.solicitud_cuenta import SolicitudCuenta

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
        # Reset DB (Drop all tables and recreate)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # 1. Roles
        print("... Creando Roles")
        roles = ["ADMINISTRADOR", "TUTOR", "VERIFICADOR", "ESTUDIANTE"]
        for nombre in roles:
            if not db.query(Rol).filter_by(nombre_rol=nombre).first():
                db.add(Rol(nombre_rol=nombre, descripcion=f"Rol de {nombre}"))
        db.commit()

        # 2. Admin User
        print("... Verificando Admin")
        rol_admin = db.query(Rol).filter_by(nombre_rol="ADMINISTRADOR").first()
        admin_user = db.query(Usuario).filter_by(correo="admin@tutorias.com").first()
        if not admin_user:
            admin_user = Usuario(
                nombres="Tulio",
                apellidos="Tribiño",
                dni="12345678",
                correo="admin@tutorias.com",
                telefono="999888777",
                contrasena_hash=hash_password("admin123"),
                id_rol=rol_admin.id_rol,
                estado="ACTIVO"
            )
            db.add(admin_user)
            db.commit()

        # 3. Semestres
        print("... Creando Semestres")
        semestres = ["2025-I", "2025-II"]
        for sem in semestres:
            if not db.query(Semestre).filter_by(codigo_semestre=sem).first():
                db.add(Semestre(codigo_semestre=sem, anio=2025, periodo=sem.split("-")[1], fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(days=120)))
        db.commit()

        # 4. Carreras
        print("... Creando Carreras")
        carreras = ["Ing. Informática y de Sistemas", "Ing. Civil", "Ing. Eléctrica"]
        for car in carreras:
            if not db.query(Carrera).filter_by(nombre_carrera=car).first():
                db.add(Carrera(nombre_carrera=car, codigo_carrera=car[:3].upper()))
        db.commit()

        # 5. Ambientes
        print("... Creando Ambientes")
        ambientes = ["201", "301", "Lab-A", "Cubil 045"]
        for amb in ambientes:
            if not db.query(Ambiente).filter_by(codigo_ambiente=amb).first():
                db.add(Ambiente(codigo_ambiente=amb, tipo="AULA", capacidad=30, ubicacion="Pabellon A"))
        db.commit()

        # 6. Tutores
        print("... Creando Tutores")
        rol_tutor = db.query(Rol).filter_by(nombre_rol="TUTOR").first()
        ambiente_def = db.query(Ambiente).first()
        carrera_is = db.query(Carrera).first()
        
        if db.query(Tutor).count() < 3:
            for i in range(3):
                u_tutor = Usuario(
                    nombres=get_random_name(),
                    apellidos=get_random_lastname(),
                    dni=f"8765432{i}",
                    correo=f"tutor{i}@unsaac.edu.pe",
                    contrasena_hash=hash_password("123456"),
                    id_rol=rol_tutor.id_rol,
                    estado="ACTIVO"
                )
                db.add(u_tutor)
                db.flush()
                tutor = Tutor(
                    id_usuario=u_tutor.id, 
                    id_carrera=carrera_is.id, 
                    id_ambiente_defecto=ambiente_def.id,
                    oficina=f"OF-{i+100}"
                )
                db.add(tutor)
        db.commit()

        # 7. Estudiantes
        print("... Creando Estudiantes")
        if db.query(Estudiante).count() < 10:
            for i in range(10):
                est = Estudiante(
                    codigo=f"22098{i}",
                    dni=f"7379264{i}",
                    nombres=get_random_name(),
                    apellidos=get_random_lastname(),
                    correo=f"alumno{i}@unsaac.edu.pe",
                    telefono=f"98765432{i}",
                    id_carrera=carrera_is.id,
                    estado_academico="REGULAR",
                    fecha_ingreso=datetime(2022, 3, 15)
                )
                db.add(est)
        db.commit()

        # 8. Clases y Asignaciones
        print("... Creando Clases")
        tutor_1 = db.query(Tutor).first()
        semestre_act = db.query(Semestre).order_by(Semestre.id.desc()).first()
        ambiente_1 = db.query(Ambiente).first()

        clase = db.query(ClaseTutoria).filter_by(nombre="Tutoría I").first()
        if not clase:
            clase = ClaseTutoria(
                nombre="Tutoría I",
                id_tutor=tutor_1.id,
                id_carrera=carrera_is.id,
                id_semestre=semestre_act.id,
                id_ambiente=ambiente_1.id
            )
            db.add(clase)
            db.flush()
            
            # Asignar estudiantes
            estudiantes = db.query(Estudiante).limit(5).all()
            for est in estudiantes:
                db.add(AsignacionTutorado(id_clase=clase.id, id_estudiante=est.id))
            db.commit()
            
            # 9. Bloque de Programacion
            print("... Creando Bloque de Programacion")
            bloque = BloqueProgramacionTutorias(
                id_carrera=carrera_is.id,
                id_semestre=semestre_act.id,
                fecha_inicio=datetime.utcnow(),
                fecha_fin=datetime.utcnow() + timedelta(days=30),
                resumen="Bloque 1 - 2025-II",
                descripcion="Primer bloque de tutorías integrales",
                creado_por=admin_user.id
            )
            db.add(bloque)
            db.commit()

            # 10. Sesiones Programadas
            print("... Creando Sesiones Programadas")
            # 1 Realizada, 1 Programada
            sesion_realizada = SesionProgramada(
                id_bloque=bloque.id,
                id_clase=clase.id,
                id_tutor=tutor_1.id,
                id_ambiente=ambiente_1.id,
                tipo_sesion="Grupal",
                fecha_hora_inicio=datetime.utcnow() - timedelta(days=7),
                fecha_hora_fin=datetime.utcnow() - timedelta(days=7, hours=-2),
                resumen="Sesión de Bienvenida (Realizada)",
                estado="REALIZADA"
            )
            db.add(sesion_realizada)
            
            sesion_programada = SesionProgramada(
                id_bloque=bloque.id,
                id_clase=clase.id,
                id_tutor=tutor_1.id,
                id_ambiente=ambiente_1.id,
                tipo_sesion="Grupal",
                fecha_hora_inicio=datetime.utcnow() + timedelta(days=2),
                fecha_hora_fin=datetime.utcnow() + timedelta(days=2, hours=2),
                resumen="Sesión de Seguimiento (Programada)",
                estado="PROGRAMADA"
            )
            db.add(sesion_programada)
            db.commit()
            
            # 11. SesionTutoria (Ejecucion) y Detalle
            print("... Registrando Ejecucion de Sesion (SesionTutoria + Detalle)")
            if sesion_realizada.id:
                # Simulamos que asistieron los 3 primeros
                for est in estudiantes[:3]:
                    st = SesionTutoria(
                        id_sesion_programada=sesion_realizada.id,
                        id_tutor=tutor_1.id,
                        id_estudiante=est.id,
                        tipo_tutoria="Grupal",
                        fecha_hora_realizacion=sesion_realizada.fecha_hora_inicio,
                        estado="REALIZADA"
                    )
                    db.add(st)
                    db.flush()
                    
                    # Detalle por estudiante
                    detalle = DetalleTutoria(
                        id_sesion_tutoria=st.id,
                        detalle_academico="El estudiante muestra buen rendimiento pero reporta estrés.",
                        observaciones_academico="Derivar a psicología si persiste.",
                        derivado_psicologia=True
                    )
                    db.add(detalle)
                    
                    # Documento Adjunto (ej. ficha de seguimiento)
                    doc = DocumentoAdjunto(
                        id_estudiante=est.id,
                        id_sesion_tutoria=st.id,
                        subido_por=tutor_1.id_usuario,
                        tipo_documento="Ficha",
                        nombre_archivo="ficha_seguimiento.pdf",
                        ruta_archivo="/files/fichas/ficha_001.pdf",
                        descripcion="Ficha de tutoría inicial"
                    )
                    db.add(doc)
            db.commit()

        # 12. Solicitudes de Cuenta
        print("... Creando Solicitudes de Cuenta")
        if not db.query(SolicitudCuenta).first():
            sol = SolicitudCuenta(
                nombres="Nuevo",
                apellidos="Docente",
                correo="nuevo.docente@unsaac.edu.pe",
                rol_solicitado="TUTOR",
                estado="PENDIENTE"
            )
            db.add(sol)
        db.commit()

        # 13. Notificaciones
        print("... Creando Notificaciones")
        if not db.query(Notificacion).first():
            notif = Notificacion(
                id_usuario_destino=tutor_1.id_usuario,
                titulo="Recordatorio de Tutoría",
                mensaje="Recuerde subir el informe de la sesión realizada.",
                tipo="INFO"
            )
            db.add(notif)
        db.commit()

        print("Datos de prueba actualizados y cargados exitosamente.")

    except Exception as e:
        print(f"Error al poblar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
