from typing import Literal, Optional
from pydantic import BaseModel, Field

class NotificacionRequest(BaseModel):
    id_reserva: int = Field(..., gt=0, description="ID de la reserva confirmada")
    canal: Literal["EMAIL", "SMS"] = Field(
        default="EMAIL",
        description="Canal de notificación a disparar (EMAIL o SMS)"
    )
    simular_fallo_proveedor: bool = Field(
        default=False,
        description="Bandera opcional para simular caída del proveedor externo en pruebas"
    )

class NotificacionData(BaseModel):
    id_notificacion: int
    tipo: str
    estado: str
    destinatario: str

class NotificacionResponse(BaseModel):
    message: str
    data: Optional[NotificacionData] = None
    success: bool