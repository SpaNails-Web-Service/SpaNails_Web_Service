from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.alerta_asignacion_schema import (
    AlertaAsignacionRequest,
    AlertaAsignacionResponse,
)
from app.services.services.alerta_asignacion_service import (
    AlertaAsignacionService,
)
from database import get_db

router = APIRouter(
    prefix="/internal/notificaciones",
    tags=["Notificaciones Internas"],
)


@router.post(
    "/asignacion",
    response_model=AlertaAsignacionResponse,
    status_code=status.HTTP_200_OK,
)
def alertar_nueva_asignacion(
    payload: AlertaAsignacionRequest,
    db: Session = Depends(get_db),
):
    return AlertaAsignacionService.alertar_asignacion(
        db=db,
        id_cita=payload.id_cita,
        id_empleado=payload.id_empleado,
        metodo=payload.metodo,
        empleado_activo=payload.empleado_activo,
    )