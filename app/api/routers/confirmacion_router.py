from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obtener_admin_actual
from app.api.schemas.confirmacion_schema import ConfirmacionData, ConfirmacionResponse
from app.services.services.reserva_service import (
    EstadoReservaNoConfirmableError,
    ReservaNoEncontradaError,
    reserva_service,
)
from database import get_db


router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


@router.patch(
    "/{id}/confirmar",
    response_model=ConfirmacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Confirmar una reserva pendiente",
    description=(
        "Cambia una reserva de Pendiente a Confirmada. Solo puede ejecutarla "
        "un administrador; una reserva Cancelada u otro estado no se puede confirmar."
    ),
    responses={
        400: {"description": "El estado actual no permite confirmar la reserva"},
        401: {"description": "Autenticación requerida o token inválido"},
        403: {"description": "Se requiere rol de administrador"},
        404: {"description": "Reserva no encontrada"},
        503: {"description": "Base de datos no disponible"},
    },
)
def confirmar_reserva(
    id: int = Path(..., ge=1, description="Identificador de la reserva"),
    _admin_id: int = Depends(obtener_admin_actual),
    db: Session = Depends(get_db),
):
    try:
        reserva = reserva_service.confirmar(db, id)
        return ConfirmacionResponse(
            message="Reserva confirmada exitosamente",
            data=ConfirmacionData(
                id_reserva=reserva.id_reserva,
                nuevo_estado=reserva.estado,
            ),
            success=True,
        )
    except ReservaNoEncontradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except EstadoReservaNoConfirmableError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible actualizar la reserva en este momento",
                "data": None,
                "success": False,
            },
        )
