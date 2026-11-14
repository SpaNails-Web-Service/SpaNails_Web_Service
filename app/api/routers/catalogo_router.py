from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from app.api.schemas.catalogo_schema import ServicioCreate, ServicioResponse, ServicioDataResponse, CatalogoResponse, ServicioCatalogoItem
from app.services.services.catalogo_service import catalogo_service

# API Catálogo: Agrupa HU-026 (POST) y HU-029 (GET)
router = APIRouter(prefix="/api/v1/catalogo", tags=["Catálogo"])

# --- HU-029: Consultar Catálogo completo ---
@router.get("", response_model=CatalogoResponse, status_code=status.HTTP_200_OK)
def consultar_catalogo():
    try:
        # 1. Solicita los servicios activos al servicio
        servicios_activos = catalogo_service.obtener_catalogo()
        
        if not servicios_activos:
            # Caso 2: No hay servicios disponibles
            return CatalogoResponse(
                mensaje="No hay servicios disponibles en este momento",
                data=[],
                success=True
            )
            
        # Caso 1 y 3: Mapeo de la lista de servicios a la estructura JSON esperada
        data_items = [
            ServicioCatalogoItem(
                id_servicio=s.id_servicio,
                nombre=s.nombre,
                precio=s.precio,
                duracion_minutos=s.duracion_minutos,
                aplica_domicilio=s.aplica_domicilio
            ) for s in servicios_activos
        ]
        
        return CatalogoResponse(
            message="Catálogo consultado exitosamente",
            data=data_items,
            success=True
        )
        
    except Exception as e:
        # Caso 5: Error de conexión simulado (HTTP 503 Service Unavailable)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "Error al intentar recuperar el catálogo de servicios.",
                "data": None,
                "success": False
            }
        )

# --- HU-026: Crear Servicio ---
@router.post("/servicios", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def registrar_servicio(
    payload: ServicioCreate,
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador' para permitir la acción")
):
    try:
        servicio_creado = catalogo_service.crear_servicio(payload, x_rol_usuario)
        
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
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except PermissionError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"mensaje": str(e), "data": None, "success": False}
        )
