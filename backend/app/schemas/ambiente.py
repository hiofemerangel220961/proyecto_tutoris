from pydantic import BaseModel


class AmbienteBase(BaseModel):
    nombre: str
    codigo: str
    tipo: str = "AULA"
    capacidad: int | None = None
    ubicacion: str | None = None
    activo: bool = True


class AmbienteCreate(AmbienteBase):
    pass


class AmbienteUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    tipo: str | None = None
    capacidad: int | None = None
    ubicacion: str | None = None
    activo: bool | None = None


class AmbienteInDBBase(AmbienteBase):
    id: int

    class Config:
        from_attributes = True


class Ambiente(AmbienteInDBBase):
    pass
