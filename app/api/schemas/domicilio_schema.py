from typing import Optional

from pydantic import BaseModel, Field


class CostoDomicilioRequest(BaseModel):
    id_direccion: int = Field(..., gt=0, description="ID de una dirección registrada del cliente")


class CostoDomicilioData(BaseModel):
    id_zona: int
    nombre_zona: str
    costo_domicilio: int = Field(..., ge=0)
    moneda: str = "COP"


class CostoDomicilioResponse(BaseModel):
    mensaje: str
    data: Optional[CostoDomicilioData] = None
    success: bool
