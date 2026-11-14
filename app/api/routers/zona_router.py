from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from app.api.schemas.zona_schema import ZonaCreate, ZonaResponse, ZonaDataResponse
from app.services.services.zona_service import zona_service

# API Logística: Endpoint para gestión de zonas
router = APIRouter(prefix="/api/v1/zonas", tags=["Logística (Zonas de Cobertura)"])

@router.post("", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
def registrar_zona(
    payload: ZonaCreate,
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador' o 'Cliente' para probar permisos")
):
    try:
        # Llamada a la capa de servicio
        zona_creada = zona_service.crear_zona(payload, x_rol_usuario)
        
        # Caso 1 y 3: Éxito (HTTP 201 Created)
        return ZonaResponse(
            message="Zona de cobertura creada exitosamente",
            data=ZonaDataResponse(
                id_zona=zona_creada.id_zona,
                nombre_zona=zona_creada.nombre_zona,
                estado=zona_creada.estado
            ),
            success=True
        )
        
    except FileExistsError as e:
        # Caso 2: Duplicidad de zona (HTTP 409 Conflict)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except PermissionError as e:
        # Permisos insuficientes (HTTP 403 Forbidden)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except ValueError as e:
        # Caso 4: Parámetro vacío (HTTP 400 Bad Request)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except Exception:
        # Caso 5: Error general de BD (HTTP 503 Service Unavailable)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"mensaje": "Error en el servidor al intentar crear la zona.", "data": None, "success": False}
        )
