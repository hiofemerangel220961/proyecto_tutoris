from pydantic import BaseModel


class CarreraBase(BaseModel):
    nombre: str
    codigo: str
    facultad: str | None = None
    activo: bool = True


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    nombre: str | None = None
    codigo: str | None = None
    facultad: str | None = None
    activo: bool | None = None


class CarreraInDBBase(CarreraBase):
    id: int

    class Config:
        from_attributes = True  # pydantic v2


class Carrera(CarreraInDBBase):
    pass
