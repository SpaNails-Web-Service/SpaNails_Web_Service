from pydantic import BaseModel, Field
from typing import Optional, Any

class ViajeFinalizarCreate(BaseModel):
    resultado: str = Field(..., description="Resultado del servicio (ej. Entregado, No entregado)")
    observaciones: Optional[str] = Field(None, max_length=255, description="Detalles adicionales del servicio")

class ViajeRespuesta(BaseModel):
    mensaje: str
    data: Optional[Any] = None
    success: bool