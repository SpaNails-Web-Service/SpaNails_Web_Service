from typing import Literal, Optional
from pydantic import BaseModel, Field


class AlertaAsignacionRequest(BaseModel):
    id_cita: int = Field(..., gt=0, description="ID de la cita/reserva asignada")
    id_empleado: int = Field(..., gt=0, description="ID del empleado/manicurista asignado")
    metodo: Literal["PUSH", "EMAIL"] = Field(
        default="PUSH",
        description="Canal de notificación a la empleada (PUSH o EMAIL)",
    )
    empleado_activo: Optional[bool] = Field(
        default=None,
        description="Bandera opcional para pruebas cuando no existe tabla/modelo de empleado",
    )


class AlertaAsignacionData(BaseModel):
    id_notificacion: int
    id_empleado: int
    metodo: str


class AlertaAsignacionResponse(BaseModel):
    message: str
    data: Optional[AlertaAsignacionData] = None
    success: bool