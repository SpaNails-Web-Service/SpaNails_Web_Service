from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AdminCreate(BaseModel):
    nombre: str = Field(..., min_length=2, example="Carlos Gerente")
    email: EmailStr = Field(..., example="carlos@spa.com")
    password: str = Field(..., min_length=6, example="admin123")
    id_rol: int = Field(..., example=2) # Ejemplo: 1=Gerente, 2=Recepcionista

class AdminDataResponse(BaseModel):
    id_admin: int
    rol: str

class AdminResponse(BaseModel):
    # Usamos Optional para manejar las dos llaves posibles de tu HU (message o mensaje)
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[AdminDataResponse]
    success: bool