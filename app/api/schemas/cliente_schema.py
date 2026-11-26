from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# Payload de entrada
class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=2, example="María Castillo")
    documento: str = Field(..., min_length=5, example="1098765432")
    email: EmailStr = Field(..., example="cliente@correo.com")
    password: str = Field(..., min_length=6, example="secreta123")

# Sub-estructura del response data
class ClienteDataResponse(BaseModel):
    id_cliente: int
    email: str
    fecha_registro: date

# Estructura del response completo (Contrato de la HU)
class ClienteResponse(BaseModel):
    message: str
    data: Optional[ClienteDataResponse]
    success: bool