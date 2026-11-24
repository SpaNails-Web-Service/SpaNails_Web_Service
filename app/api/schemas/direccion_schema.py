from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any

class DireccionCreate(BaseModel):
    direccion: str = Field(..., description="Nomenclatura principal")
    barrio: str = Field(..., description="Barrio de residencia")
    municipio_id: int = Field(..., description="ID del municipio")
    observaciones: Optional[str] = Field(None, description="Detalles adicionales")

    @field_validator("direccion")
    def validar_nomenclatura(cls, v):
        if not v or not v.strip():
            raise ValueError("La nomenclatura de la dirección es obligatoria")
        return v

class DireccionResponse(BaseModel):
    message: Optional[str] = None
    mensaje: Optional[str] = None 
    data: Optional[Any] = None
    success: bool