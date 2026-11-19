from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class AlertaCancelacionRequest(BaseModel):
    id_cita: int = Field(..., gt=0, description="ID de la cita cancelada")
    canal: Literal["EMAIL", "PUSH"] = Field(
        default="EMAIL",
        description="Canal de alerta (EMAIL o PUSH)",
    )


class AlertaCancelacionData(BaseModel):
    alertas_generadas: int
    destinos: List[str]


class AlertaCancelacionResponse(BaseModel):
    message: str
    data: Optional[AlertaCancelacionData] = None
    success: bool