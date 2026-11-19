from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ServicioEnReserva(BaseModel):
    id_servicio: int = Field(..., gt=0)


class ReservaCreate(BaseModel):
    servicios: list[ServicioEnReserva] = Field(..., min_length=1)
    fecha: date
    hora_inicio: time
    modalidad: str
    id_direccion: Optional[int] = Field(default=None, gt=0)

    @field_validator("modalidad")
    @classmethod
    def normalizar_modalidad(cls, valor: str) -> str:
        modalidad = valor.strip().lower()
        if modalidad in {"spa", "en el spa"}:
            return "En el spa"
        if modalidad in {"domicilio", "a domicilio"}:
            return "A domicilio"
        raise ValueError("La modalidad debe ser 'En el spa' o 'A domicilio'")


class ServicioReservaResponse(BaseModel):
    id_servicio: int
    nombre: str
    precio: float
    duracion_minutos: int


class ReservaDataResponse(BaseModel):
    id_reserva: int
    estado: str
    fecha: date
    hora_inicio: str
    modalidad: str
    servicios: list[ServicioReservaResponse]
    id_direccion: Optional[int] = None
    subtotal: float
    costo_domicilio: int
    total: float
    moneda: str


class ReservaResponse(BaseModel):
    mensaje: str
    data: Optional[ReservaDataResponse] = None
    success: bool
