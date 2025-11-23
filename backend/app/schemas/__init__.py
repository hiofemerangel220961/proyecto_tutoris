from .auth import (
    LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
    ForgotPasswordRequest, ResetPasswordRequest, UsuarioBase
)
from .carrera import CarreraCreate, CarreraRead, CarreraUpdate
from .semestre import SemestreCreate, SemestreRead, SemestreUpdate
from .ambiente import AmbienteCreate, AmbienteRead, AmbienteUpdate
from .usuario import UsuarioMinimo
from .tutor import TutorCreate, TutorRead
from .estudiante import EstudianteCreate, EstudianteRead
from .clase import ClaseCreate, ClaseRead, ClaseUpdate