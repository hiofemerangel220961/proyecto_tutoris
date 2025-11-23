from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db.deps import get_db
from ...schemas.auth import (
    LoginRequest, LoginResponse,
    RegisterRequest, RegisterResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse,
)
# Importamos nuestro nuevo servicio
from ...services.auth import AuthService

router = APIRouter()

# Configuración de templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ==========================================
#  RUTAS DE VISTAS (HTML) - GET
# ==========================================

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.get("/forgot-password")
def forgot_password_page(request: Request):
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})

@router.get("/reset-password")
def reset_password_page(request: Request):
    return templates.TemplateResponse("auth/reset_password.html", {"request": request})

# ==========================================
#  RUTAS DE API (LÓGICA) - POST
# ==========================================

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Delegamos al servicio
    usuario_logueado = AuthService.authenticate_user(db, data)
    return LoginResponse(usuario=usuario_logueado)

@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Delegamos al servicio
    return AuthService.register_user_solicitude(db, data)

@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Delegamos al servicio
    return AuthService.request_password_reset(db, data)

@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Delegamos al servicio
    return AuthService.perform_reset_password(db, data)