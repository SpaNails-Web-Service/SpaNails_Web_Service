from pydantic import BaseModel, Field
from typing import Optional

class ResenaCreate(BaseModel):
    id_cita: int
    calificacion: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None

class ResenaDataResponse(BaseModel):
    id_resena: int
    calificacion: int

class ResenaResponse(BaseModel):
    message: str
    data: Optional[ResenaDataResponse] = None
    success: bool

