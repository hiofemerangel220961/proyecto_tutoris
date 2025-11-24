import sys
import os
from datetime import date, datetime

# Aseguramos que Python encuentre el módulo 'backend'
sys.path.append(os.getcwd())

from backend.app.db.database import SessionLocal, engine, Base
from backend.app.models.usuario import Usuario
from backend.app.models.rol import Rol
from backend.app.models.carrera import Carrera
from backend.app.models.semestre import Semestre
from backend.app.models.tutor import Tutor
from backend.app.models.clase_tutoria import ClaseTutoria
from backend.app.models.ambiente import Ambiente
from backend.app.models.estudiante import Estudiante
from backend.app.models.asignacion_tutorado import AsignacionTutorado
from backend.app.core.security import hash_password

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("🌱 Iniciando carga de datos...")

# 1. Carreras
c1 = db.query(Carrera).filter_by(codigo="IIS").first()
if not c1:
    c1 = Carrera(nombre="Ing. Informática y de Sistemas", codigo="IIS", facultad="Ingeniería")
    db.add(c1)

c2 = db.query(Carrera).filter_by(codigo="IC").first()
if not c2:
    c2 = Carrera(nombre="Ing. Civil", codigo="IC", facultad="Ingeniería")
    db.add(c2)
db.commit()

# Recargar objetos para asegurar que tenemos los IDs
db.refresh(c1)
db.refresh(c2)

# 2. Semestre
sem = db.query(Semestre).filter_by(codigo="2025-II").first()
if not sem:
    sem = Semestre(
        codigo="2025-II", 
        anio=2025, 
        periodo="II", 
        fecha_inicio=date(2025, 8, 1), 
        fecha_fin=date(2025, 12, 20), 
        activo=True, 
        estado_actual="ACTIVO"
    )
    db.add(sem)
    db.commit()
db.refresh(sem)

# 3. Ambiente
amb = db.query(Ambiente).filter_by(codigo="101").first()
if not amb:
    amb = Ambiente(nombre="Aula 101", codigo="101", tipo="AULA", capacidad=30)
    db.add(amb)
    db.commit()
db.refresh(amb)

# 4. Roles
roles = ["ADMINISTRADOR", "TUTOR", "VERIFICADOR"]
for r in roles:
    existe = db.query(Rol).filter_by(nombre_rol=r).first()
    if not existe:
        db.add(Rol(nombre_rol=r, descripcion=f"Rol {r}"))
db.commit()

rol_tutor = db.query(Rol).filter_by(nombre_rol="TUTOR").first()

# 5. Tutores y Clases
tutores_data = [
    ("Juan Carlos", "Bodoque"),
    ("Tulio", "Tribiño"),
    ("Juanin", "Juan Harry")
]

for nombre, apellido in tutores_data:
    email_limpio = f"{nombre.lower().replace(' ', '')}@unsaac.edu.pe"
    
    # Usuario
    usuario = db.query(Usuario).filter(Usuario.correo == email_limpio).first()
    if not usuario:
        usuario = Usuario(
            nombres=nombre, 
            apellidos=apellido, 
            correo=email_limpio, 
            telefono="987654321",
            contrasena_hash=hash_password("123"), # Contraseña genérica
            id_rol=rol_tutor.id_rol, 
            estado="ACTIVO"
        )
        db.add(usuario)
        db.commit()
        print(f"👤 Usuario creado: {nombre} ({email_limpio})")
    
    # Recargar usuario
    db.refresh(usuario)

    # Tutor
    tutor = db.query(Tutor).filter(Tutor.id_usuario == usuario.id_usuario).first()
    
    # CORRECCIÓN AQUÍ: Usamos .id en lugar de .id_carrera para el objeto Python
    carrera_asignada = c1 if "Juan" in nombre else c2
    
    if not tutor:
        tutor = Tutor(
            id_usuario=usuario.id_usuario, 
            id_carrera=carrera_asignada.id,  # <--- CORREGIDO (antes .id_carrera)
            codigo_docente=f"DOC-{usuario.id_usuario}"
        )
        db.add(tutor)
        db.commit()
    
    db.refresh(tutor)

    # Clase
    nombre_clase = f"Tutoría {nombre}"
    clase = db.query(ClaseTutoria).filter_by(nombre=nombre_clase).first()
    if not clase:
        clase = ClaseTutoria(
            nombre=nombre_clase, 
            id_tutor=tutor.id,          # <--- CORREGIDO (antes .id_tutor)
            id_carrera=carrera_asignada.id, # <--- CORREGIDO
            id_semestre=sem.id,         # <--- CORREGIDO (antes .id_semestre)
            id_ambiente=amb.id,         # <--- CORREGIDO (antes .id_ambiente)
            activo=True
        )
        db.add(clase)
        db.commit()
        print(f"   📚 Clase creada: {nombre_clase}")

    db.refresh(clase)

    # 6. Estudiantes y Asignación (Agregar 2 alumnos por clase)
    for i in range(1, 3):
        # Generamos un código único para no chocar
        codigo_est = f"{carrera_asignada.codigo}25{tutor.id}{i}"
        est = db.query(Estudiante).filter_by(codigo=codigo_est).first()
        
        if not est:
            est = Estudiante(
                codigo=codigo_est,
                dni=f"7000{tutor.id}{i}",
                nombres=f"Alumno{i}",
                apellidos=f"De {nombre}",
                correo=f"alumno{i}.{nombre.lower().replace(' ', '')}@est.unsaac.edu.pe",
                id_carrera=carrera_asignada.id, # <--- CORREGIDO
                estado_academico="REGULAR"
            )
            db.add(est)
            db.commit()
        
        db.refresh(est)
        
        # Asignar a la clase
        asignacion = db.query(AsignacionTutorado).filter_by(id_clase=clase.id, id_estudiante=est.id).first()
        if not asignacion:
            asignacion = AsignacionTutorado(
                id_clase=clase.id,          # <--- CORREGIDO
                id_estudiante=est.id,       # <--- CORREGIDO (antes .id_estudiante)
                estado="VIGENTE"
            )
            db.add(asignacion)
            db.commit()
            print(f"      🎓 Alumno asignado: {est.nombres} {est.apellidos}")

print("✅ Datos verificados y creados exitosamente.")
db.close()