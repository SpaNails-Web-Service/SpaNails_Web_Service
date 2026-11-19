from datetime import date
from typing import Optional

from pydantic import BaseModel


class HorarioDisponible(BaseModel):
    hora_inicio: str
    hora_fin: str


class DisponibilidadData(BaseModel):
    fecha: date
    id_servicio: int
    modalidad: str
    horarios_disponibles: list[HorarioDisponible]


class DisponibilidadResponse(BaseModel):
    mensaje: str
    data: Optional[DisponibilidadData] = None
    success: bool
