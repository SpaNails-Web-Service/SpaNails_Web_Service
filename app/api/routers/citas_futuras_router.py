from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obtener_cliente_actual
from app.api.schemas.citas_futuras_schema import (
    CitasFuturasResponse,
    CitasFuturasVaciasResponse,
)
from app.services.services.reserva_service import reserva_service
from database import get_db


router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


@router.get(
    "/futuras",
    response_model=CitasFuturasResponse | CitasFuturasVaciasResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar las citas futuras del cliente autenticado",
    description=(
        "Lista en orden cronológico las reservas Pendientes o Confirmadas del cliente "
        "cuya fecha y hora de inicio sean posteriores al momento actual."
    ),
    responses={
        401: {"description": "Autenticación requerida o token inválido"},
        503: {"description": "Base de datos no disponible"},
    },
)
def consultar_citas_futuras(
    cliente_id: int = Depends(obtener_cliente_actual),
    db: Session = Depends(get_db),
):
    try:
        citas = reserva_service.listar_citas_futuras(db, cliente_id)
        if not citas:
            return CitasFuturasVaciasResponse(
                mensaje="No tienes citas futuras programadas",
                data=[],
                success=True,
            )
        return CitasFuturasResponse(
            message="Citas futuras consultadas",
            data=citas,
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible consultar las citas futuras en este momento",
                "data": None,
                "success": False,
            },
        )
