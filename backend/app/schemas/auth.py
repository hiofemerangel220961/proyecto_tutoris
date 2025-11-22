from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str


class UsuarioBase(BaseModel):
    id_usuario: int
    nombres: str
    apellidos: str
    correo: EmailStr
    estado: str
    rol: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    usuario: UsuarioBase
