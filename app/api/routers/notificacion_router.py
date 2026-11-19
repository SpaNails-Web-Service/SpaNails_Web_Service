from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.notificacion_schema import NotificacionRequest, NotificacionResponse
from app.services.services.notificacion_service import NotificacionService
from database import get_db

router = APIRouter(
    prefix="/internal/notificaciones",
    tags=["Notificaciones Internas"]
)

@router.post("/confirmacion", response_model=NotificacionResponse, status_code=status.HTTP_200_OK)
def transmitir_confirmacion_reserva(
    payload: NotificacionRequest,
    db: Session = Depends(get_db)
):
    return NotificacionService.transmitir_confirmacion(
        db=db,
        id_reserva=payload.id_reserva,
        canal=payload.canal,
        simular_fallo_proveedor=payload.simular_fallo_proveedor
    )