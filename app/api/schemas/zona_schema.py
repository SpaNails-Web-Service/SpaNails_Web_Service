from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ZonaCreate(BaseModel):
    nombre_zona: str = Field(..., example="Cabecera")

    @field_validator('nombre_zona')
    @classmethod
    def nombre_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre de la zona no puede estar vacío")
        return v

class ZonaDataResponse(BaseModel):
    id_zona: int
    nombre_zona: str
    estado: str

class ZonaResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None
    data: Optional[ZonaDataResponse]
    success: bool
