from fastapi import APIRouter, Header, status, Query
from fastapi.responses import JSONResponse
from app.api.schemas.zona_schema import (
    ZonaCreate, ZonaResponse, ZonaDataResponse,
    CoberturaResponse, CoberturaDataResponse
)
from app.services.services.zona_service import zona_service

# API Logística: Zonas de Cobertura
router = APIRouter(prefix="/api/v1/zonas", tags=["Logística (Zonas de Cobertura)"])

# --- HU-038: Comprobar Cobertura ---
@router.get("/validar", response_model=CoberturaResponse, status_code=status.HTTP_200_OK)
def validar_cobertura(
    ubicacion: str = Query(None, description="Nombre del barrio o coordenadas a validar (Ej: 'Cabecera')")
):
    try:
        # Caso 4: Parámetros omitidos o vacíos
        if not ubicacion:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"mensaje": "Debe proporcionar una ubicación válida", "data": None, "success": False}
            )

        # 1. Llamada a la capa de servicio
        zona_cobertura = zona_service.validar_cobertura(ubicacion)
        
        # Caso 1 y 3: Hay cobertura (HTTP 200 OK)
        if zona_cobertura:
            return CoberturaResponse(
                message="Cobertura confirmada",
                data=CoberturaDataResponse(
                    cobertura_disponible=True,
                    id_zona=zona_cobertura.id_zona,
                    nombre_zona=zona_cobertura.nombre_zona
                ),
                success=True
            )
        
        # Caso 2: No hay cobertura (HTTP 200 OK)
        return CoberturaResponse(
            mensaje="Lo sentimos, no tenemos cobertura en la dirección indicada",
            data=CoberturaDataResponse(cobertura_disponible=False),
            success=True
        )
        
    except ValueError as e:
        # Manejo de reglas de negocio para Caso 4
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except Exception:
        # Caso 5: Fallo de BD (HTTP 503)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"mensaje": "Error interno al validar la cobertura logística.", "data": None, "success": False}
        )

# --- HU-036: Crear Zona ---
@router.post("", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
def registrar_zona(
    payload: ZonaCreate,
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador'")
):
    try:
        zona_creada = zona_service.crear_zona(payload, x_rol_usuario)
        return ZonaResponse(
            message="Zona de cobertura creada exitosamente",
            data=ZonaDataResponse(
                id_zona=zona_creada.id_zona,
                nombre_zona=zona_creada.nombre_zona,
                estado=zona_creada.estado,
                tarifa_domicilio=zona_creada.tarifa_domicilio,
            ),
            success=True
        )
    except FileExistsError as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"mensaje": str(e), "data": None, "success": False})
    except PermissionError as e:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"mensaje": str(e), "data": None, "success": False})
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"mensaje": str(e), "data": None, "success": False})
    except Exception:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"mensaje": "Error en el servidor al intentar crear la zona.", "data": None, "success": False})
