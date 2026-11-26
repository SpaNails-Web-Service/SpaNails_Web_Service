from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.schemas.cita_tiempo_schema import (
    CalcularTiempoFinRequest,
    CalcularTiempoFinResponse,
    CalcularTiempoFinData,
)
from app.services.services.cita_tiempo_service import (
    DuracionNoConfiguradaError,
    InicioEnElPasadoError,
    ModalidadNoDisponibleError,
    ServicioNoEncontradoError,
    ServicioNoDisponibleError,
    cita_tiempo_service,
)


router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


@router.post(
    "/calcular-tiempo-fin",
    response_model=CalcularTiempoFinResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcular fin del servicio y bloqueo de agenda",
    description=(
        "Suma las duraciones vigentes de los servicios activos y agrega 20 minutos "
        "al bloqueo de agenda. No crea ni modifica una reserva."
    ),
    responses={
        400: {"description": "Fecha, hora, servicio o modalidad inválidos"},
        404: {"description": "Uno de los servicios no existe"},
    },
)
def calcular_tiempo_fin(solicitud: CalcularTiempoFinRequest):
    try:
        resultado = cita_tiempo_service.calcular(solicitud)
        return CalcularTiempoFinResponse(
            mensaje="Tiempo de finalización calculado exitosamente",
            data=CalcularTiempoFinData(**resultado),
            success=True,
        )
    except ServicioNoEncontradoError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except (
        ServicioNoDisponibleError,
        DuracionNoConfiguradaError,
        InicioEnElPasadoError,
        ModalidadNoDisponibleError,
    ) as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
