from typing import Literal, Optional
from pydantic import BaseModel, Field


class AlertaLogisticaRequest(BaseModel):
    id_cita: int = Field(..., gt=0, description="ID de la cita/reserva en camino")
    canal: Literal["EMAIL", "SMS"] = Field(
        default="SMS",
        description="Canal de notificación al cliente (EMAIL o SMS)",
    )
    distancia_km: Optional[float] = Field(
        default=None,
        gt=0,
        description="Distancia opcional en km para pruebas o cálculo directo",
    )
    velocidad_promedio_kmh: float = Field(
        default=24.0,
        gt=0,
        description="Velocidad promedio urbana estimada en km/h",
    )


class AlertaLogisticaData(BaseModel):
    id_notificacion: int
    estado: str
    tiempo_estimado_minutos: int


class AlertaLogisticaResponse(BaseModel):
    message: str
    data: Optional[AlertaLogisticaData] = None
    success: bool