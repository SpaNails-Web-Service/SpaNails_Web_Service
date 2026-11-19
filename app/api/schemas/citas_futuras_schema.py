from pydantic import BaseModel


class CitaFuturaItem(BaseModel):
    id_reserva: int
    fecha_inicio: str
    servicio: str
    manicurista: str | None = None
    estado: str


class CitasFuturasResponse(BaseModel):
    message: str
    data: list[CitaFuturaItem]
    success: bool


class CitasFuturasVaciasResponse(BaseModel):
    mensaje: str
    data: list[CitaFuturaItem]
    success: bool
