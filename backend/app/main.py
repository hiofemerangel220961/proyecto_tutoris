from fastapi import FastAPI
from .db.database import Base, engine
from .models import rol, usuario  # importa para que registren las tablas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Tutorías")

@app.get("/")
def root():
    return {"message": "API del Sistema de Tutorías funcionando"}

@app.get("/health")
def health_check():
    return {"status": "ok"}