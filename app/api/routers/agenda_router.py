from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.dependencies.auth import bearer_scheme, obtener_cliente_actual
from app.api.schemas.disponibilidad_schema import DisponibilidadResponse
from app.services.services.disponibilidad_service import (
    DireccionNoEncontradaError,
    FechaNoValidaError,
    FueraDeCoberturaError,
    ModalidadNoDisponibleError,
    ServicioNoEncontradoError,
    ServicioNoDisponibleError,
    disponibilidad_service,
)
from database import get_db


router = APIRouter(prefix="/api/v1/agenda", tags=["Agenda"])


@router.get(
    "/disponibilidad",
    response_model=DisponibilidadResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar disponibilidad de agenda",
    description=(
        "Devuelve inicios cada 30 minutos dentro del horario laboral. "
        "Cada bloque respeta la duración del servicio y los 20 minutos adicionales. "
        "La consulta no crea ni bloquea una reserva."
    ),
    responses={
        400: {"description": "Fecha, modalidad, cobertura o servicio inválidos"},
        401: {"description": "Se requiere autenticación para consultar domicilio"},
        404: {"description": "Servicio o dirección inexistente"},
    },
)
def consultar_disponibilidad(
    id_servicio: int = Query(..., gt=0),
    fecha: str = Query(..., description="Fecha futura en formato AAAA-MM-DD"),
    modalidad: str = Query(..., description="'spa'/'En el spa' o 'domicilio'/'A domicilio'"),
    id_direccion: int | None = Query(default=None, gt=0),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        try:
            fecha_consulta = date.fromisoformat(fecha)
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "mensaje": "La fecha debe tener formato AAAA-MM-DD",
                    "data": None,
                    "success": False,
                },
            )

        user_id = None
        if modalidad.strip().lower() in {"domicilio", "a domicilio"}:
            user_id = obtener_cliente_actual(credentials)

        resultado = disponibilidad_service.consultar(
            db=db,
            id_servicio=id_servicio,
            fecha=fecha_consulta,
            modalidad=modalidad,
            id_direccion=id_direccion,
            user_id=user_id,
        )
        return DisponibilidadResponse(**resultado)
    except ServicioNoEncontradoError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except DireccionNoEncontradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except (
        ValueError,
        FechaNoValidaError,
        ServicioNoDisponibleError,
        ModalidadNoDisponibleError,
        FueraDeCoberturaError,
    ) as exc:
        status_code = (
            status.HTTP_401_UNAUTHORIZED
            if "iniciar sesión" in str(exc).lower()
            else status.HTTP_400_BAD_REQUEST
        )
        return JSONResponse(
            status_code=status_code,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
