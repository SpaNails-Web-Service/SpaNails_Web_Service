from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

# Esquemas Logística general
from app.api.schemas.domicilio_schema import (
    CostoDomicilioData,
    CostoDomicilioRequest,
    CostoDomicilioResponse,
)
# esquemas para la HU-048
from app.api.schemas.fin_servicio_schema import ViajeFinalizarCreate, ViajeRespuesta

from app.api.dependencies.auth import obtener_cliente_actual
from app.services.services.domicilio_service import (
    DireccionNoEncontradaError,
    FueraDeCoberturaError,
    TarifaNoConfiguradaError,
    domicilio_service,
)

# Tu servicio y repositorio de viajes para la HU-048
from app.services.services.fin_servicio_service import ViajeService
from app.repositories.repositories.fin_servicio_repository import ViajeRepository
from database import get_db


router = APIRouter(prefix="/api/v1/logistica", tags=["Logística"])

# Instancia del servicio de viajes para la HU-048
viaje_repo = ViajeRepository()
viaje_service = ViajeService(viaje_repo)


# ==========================================
# ENDPOINT DE TU COMPAÑERO (Costo Domicilio)
# ==========================================
@router.post(
    "/costo-domicilio",
    response_model=CostoDomicilioResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcular costo de domicilio",
    description=(
        "Calcula el costo según la zona activa de una dirección del cliente. "
        "No crea reservas ni registra cobros. Requiere token Bearer."
    ),
    responses={
        400: {"description": "La dirección está fuera de cobertura"},
        401: {"description": "Autenticación requerida o token inválido"},
        404: {"description": "Dirección inexistente o no perteneciente al cliente"},
        409: {"description": "La zona no tiene tarifa configurada"},
        503: {"description": "Base de datos o servicio logístico no disponible"},
    },
)
def calcular_costo_domicilio(
    payload: CostoDomicilioRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(obtener_cliente_actual),
):
    try:
        costo = domicilio_service.calcular_costo(db, user_id, payload.id_direccion)
        return CostoDomicilioResponse(
            mensaje="Costo de domicilio calculado exitosamente",
            data=CostoDomicilioData(**costo),
            success=True,
        )
    except DireccionNoEncontradaError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except FueraDeCoberturaError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except TarifaNoConfiguradaError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": str(exc), "data": None, "success": False},
        )
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible consultar la dirección en este momento",
                "data": None,
                "success": False,
            },
        )


# ==========================================
# TU ENDPOINT DE LA HU-048 (Finalizar Viaje)
# ==========================================
@router.post(
    "/viajes/{id_viaje}/finalizar",
    response_model=ViajeRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Finalizar servicio logístico",
    description="Permite al domiciliario asignado o administrador finalizar el servicio logístico actualizando su estado."
)
def finalizar_servicio_logistico(
    id_viaje: int,
    datos: ViajeFinalizarCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(obtener_cliente_actual),
):
    try:
        # Aquí puedes empaquetar el usuario actual con el ID que te devuelve la dependencia de autenticación
        usuario_actual = {"id": usuario_id, "roles": ["Administrador", "Domiciliario"], "activo": True}
        
        return viaje_service.finalizar_viaje(db=db, id_viaje=id_viaje, datos=datos, usuario_actual=usuario_actual)

    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "No fue posible finalizar el servicio logístico en este momento",
                "data": None,
                "success": False,
            },
        )