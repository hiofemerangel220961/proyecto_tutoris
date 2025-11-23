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
        # aviso de pydantic v2, pero sigue funcionando
        from_attributes = True


class LoginResponse(BaseModel):
    usuario: UsuarioBase


# ---------- Registro (crear cuenta) ----------

class RegisterRequest(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr
    rol_solicitado: str  # "ADMINISTRADOR", "TUTOR" o "VERIFICADOR"


class RegisterResponse(BaseModel):
    id_solicitud: int
    estado: str
    mensaje: str

# ---------- Recuperar / cambiar contraseña ----------

class ForgotPasswordRequest(BaseModel):
    correo: EmailStr


class ForgotPasswordResponse(BaseModel):
    mensaje: str


class ResetPasswordRequest(BaseModel):
    token: str
    nueva_contrasena: str


class ResetPasswordResponse(BaseModel):
    mensaje: str