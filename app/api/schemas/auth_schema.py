from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="cliente@correo.com")
    password: str = Field(..., example="secreta123")

    @field_validator('password')
    @classmethod
    def password_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("La contraseña es obligatoria para iniciar sesión.")
        return v

class LoginDataResponse(BaseModel):
    token: str
    id_usuario: int
    rol: str

class LoginResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[LoginDataResponse]
    success: bool
