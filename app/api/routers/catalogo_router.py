from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from app.api.schemas.catalogo_schema import ServicioCreate, ServicioResponse, ServicioDataResponse
from app.services.services.catalogo_service import catalogo_service

# API Catálogo: Endpoint para registrar servicios
router = APIRouter(prefix="/api/v1/catalogo", tags=["Catálogo"])

@router.post("/servicios", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def registrar_servicio(
    payload: ServicioCreate,
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador' para permitir la acción")
):
    try:
        # 1. Llamada a la capa de servicio
        servicio_creado = catalogo_service.crear_servicio(payload, x_rol_usuario)
        
        # 2. Caso de éxito (HTTP 201 Created)
        return ServicioResponse(
            message="Servicio registrado exitosamente",
            data=ServicioDataResponse(
                id_servicio=servicio_creado.id_servicio,
                nombre=servicio_creado.nombre,
                estado=servicio_creado.estado
            ),
            success=True
        )
        
    except FileExistsError as e:
        # 3. Caso de error por duplicidad (HTTP 409 Conflict)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
    except PermissionError as e:
        # 4. Caso de permisos insuficientes (HTTP 403 Forbidden)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
    except ValueError as e:
        # 5. Caso de regla de negocio (precio <= 0) (HTTP 400 Bad Request)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
