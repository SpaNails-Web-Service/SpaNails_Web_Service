from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.alerta_cancelacion_schema import (
    AlertaCancelacionRequest,
    AlertaCancelacionResponse,
)
from app.services.services.alerta_cancelacion_service import (
    AlertaCancelacionService,
)
from database import get_db

router = APIRouter(
    prefix="/internal/notificaciones",
    tags=["Notificaciones Internas"],
)


@router.post(
    "/cancelacion",
    response_model=AlertaCancelacionResponse,
    status_code=status.HTTP_200_OK,
)
def alertar_cancelacion_cita(
    payload: AlertaCancelacionRequest,
    db: Session = Depends(get_db),
):
    return AlertaCancelacionService.alertar_cancelacion(
        db=db,
        id_cita=payload.id_cita,
        canal=payload.canal,
    )