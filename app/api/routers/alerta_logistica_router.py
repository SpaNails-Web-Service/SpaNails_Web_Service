from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.alerta_logistica_schema import (
    AlertaLogisticaRequest,
    AlertaLogisticaResponse,
)
from app.services.services.alerta_logistica_service import (
    AlertaLogisticaService,
)
from database import get_db

router = APIRouter(
    prefix="/internal/notificaciones",
    tags=["Notificaciones Internas"],
)


@router.post(
    "/logistica",
    response_model=AlertaLogisticaResponse,
    status_code=status.HTTP_200_OK,
)
def transmitir_alerta_logistica(
    payload: AlertaLogisticaRequest,
    db: Session = Depends(get_db),
):
    return AlertaLogisticaService.alertar_estado_logistico(
        db=db,
        id_cita=payload.id_cita,
        canal=payload.canal,
        distancia_km=payload.distancia_km,
        velocidad_promedio_kmh=payload.velocidad_promedio_kmh,
    )