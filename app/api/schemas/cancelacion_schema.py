from pydantic import BaseModel


class CancelacionData(BaseModel):
    id_reserva: int
    nuevo_estado: str
    penalidad: bool


class CancelacionResponse(BaseModel):
    message: str
    data: CancelacionData
    success: bool
