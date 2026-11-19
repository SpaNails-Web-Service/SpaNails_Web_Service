from datetime import date, time
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ServicioSeleccionado(BaseModel):
    id_servicio: int = Field(..., gt=0, description="Identificador del servicio del catálogo")


class CalcularTiempoFinRequest(BaseModel):
    servicios: list[ServicioSeleccionado] = Field(
        ..., min_length=1, description="Uno o varios servicios activos"
    )
    fecha: date
    hora_inicio: time
    modalidad: Literal["En el spa", "A domicilio"]


class CalcularTiempoFinData(BaseModel):
    hora_inicio: str
    duracion_total_servicios_minutos: int
    hora_fin_servicio: str
    tiempo_adicional_minutos: int
    hora_fin_bloqueo_agenda: str


class CalcularTiempoFinResponse(BaseModel):
    mensaje: str
    data: Optional[CalcularTiempoFinData] = None
    success: bool
