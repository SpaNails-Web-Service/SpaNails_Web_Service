from pydantic import BaseModel, Field
from typing import List, Optional, Any

class CitaManicuristaItem(BaseModel):
    id_reserva: int = Field(..., description="ID de la reserva")
    cliente: str = Field(..., description="Nombre del cliente")
    hora_inicio: str = Field(..., description="Hora de inicio de la cita (HH:MM:SS)")
    servicio: str = Field(..., description="Nombre del servicio")
    modalidad: str = Field(..., description="Modalidad del servicio (ej. Domicilio)")

class EmpleadoCitasRespuesta(BaseModel):
    message: Optional[str] = Field(None, description="Mensaje descriptivo")
    mensaje: Optional[str] = Field(None, description="Mensaje alternativo para agendas vacías")
    data: List[CitaManicuristaItem] = Field(..., description="Lista de citas asignadas")
    success: bool = Field(..., description="Estado de éxito de la operación")