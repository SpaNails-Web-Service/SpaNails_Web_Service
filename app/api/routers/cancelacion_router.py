from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obtener_cliente_actual
from app.api.schemas.cancelacion_schema import CancelacionData, CancelacionResponse
from app.services.services.reserva_service import (
    EstadoReservaNoCancelableError,
    ReservaNoAutorizadaError,
    ReservaNoEncontradaError,
    reserva_service,
)
from database import get_db


router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


@router.patch(
    "/{id}/cancelar",
    response_model=CancelacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Anular una reserva del cliente autenticado",
    description=(
        "Permite cancelar reservas Pendientes o Confirmadas que aún no han comenzado. "
        "La cancelación con menos de 24 horas de anticipación marca penalidad=true. "
        "Al cancelar, el bloque se libera en la agenda."
    ),
    responses={
        400: {"description": "La reserva ya fue cancelada, terminó o no permite cancelación"},
        401: {"description": "Autenticación requerida o token inválido"},
        403: {"description": "La reserva pertenece a otro cliente"},
        404: {"description": "Reserva no encontrada"},
        503: {"description": "Base de datos no disponible"},
    },
)
def cancelar_reserva(
    id: int = Path(..., ge=1, description="Identificador de la reserva"),
    cliente_id: int = Depends(obtener_cliente_actual),
    db: Session = Depends(get_db),
):
    try:
        reserva, penalidad = reserva_service.cancelar(db, id, cliente_id)
        mensaje = "Su cita ha sido anulada exitosamente"
        if penalidad:
            mensaje += ". Se aplicará la política de cancelación por estar dentro de las 24 horas"
        return CancelacionResponse(
            message=mensaje,
            data=CancelacionData(
                id_reserva=reserva.id_reserva,
                nuevo_estado=reserva.estado,
                penalidad=penalidad,
            ),
            success=True,
        )
    except ReservaNoEncontradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except ReservaNoAutorizadaError as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except EstadoReservaNoCancelableError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible cancelar la reserva en este momento",
                "data": None,
                "success": False,
            },
        )
