from pydantic import BaseModel


class ConfirmacionData(BaseModel):
    id_reserva: int
    nuevo_estado: str


class ConfirmacionResponse(BaseModel):
    message: str
    data: ConfirmacionData
    success: bool
