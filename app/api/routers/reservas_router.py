from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obtener_cliente_actual
from app.api.schemas.reserva_schema import (
    ReservaCreate,
    ReservaDataResponse,
    ReservaResponse,
    ServicioReservaResponse,
)
from app.services.services.domicilio_service import (
    DireccionNoEncontradaError,
    FueraDeCoberturaError,
    TarifaNoConfiguradaError,
)
from app.services.services.reserva_service import (
    FechaReservaInvalidaError,
    HorarioNoDisponibleError,
    ModalidadReservaNoDisponibleError,
    ServicioReservaNoDisponibleError,
    ServicioReservaNoEncontradoError,
    reserva_service,
)
from database import get_db


router = APIRouter(prefix="/api/v1/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear reserva de servicio",
    description=(
        "Crea una reserva para el cliente autenticado. Revalida la agenda, "
        "calcula los precios desde el catálogo y, para domicilio, consulta la tarifa vigente."
    ),
    responses={
        400: {"description": "Datos, servicio o modalidad inválidos"},
        401: {"description": "Autenticación requerida"},
        404: {"description": "Servicio o dirección inexistente"},
        409: {"description": "El horario está ocupado o no hay tarifa configurada"},
        503: {"description": "No fue posible guardar la reserva"},
    },
)
def crear_reserva(
    solicitud: ReservaCreate,
    cliente_id: int = Depends(obtener_cliente_actual),
    db: Session = Depends(get_db),
):
    try:
        reserva = reserva_service.crear(db, cliente_id, solicitud)
        data = ReservaDataResponse(
            id_reserva=reserva.id_reserva,
            estado=reserva.estado,
            fecha=reserva.fecha,
            hora_inicio=reserva.hora_inicio,
            modalidad=reserva.modalidad,
            servicios=[ServicioReservaResponse(**item) for item in reserva.servicios_detalle],
            id_direccion=reserva.id_direccion,
            subtotal=reserva.subtotal,
            costo_domicilio=reserva.costo_domicilio,
            total=reserva.total,
            moneda=reserva.moneda,
        )
        return ReservaResponse(
            mensaje="Reserva creada exitosamente",
            data=data,
            success=True,
        )
    except ServicioReservaNoEncontradoError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except DireccionNoEncontradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except HorarioNoDisponibleError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except TarifaNoConfiguradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except (
        ValueError,
        FechaReservaInvalidaError,
        FueraDeCoberturaError,
        ModalidadReservaNoDisponibleError,
        ServicioReservaNoDisponibleError,
    ) as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible guardar la reserva en este momento",
                "data": None,
                "success": False,
            },
        )
