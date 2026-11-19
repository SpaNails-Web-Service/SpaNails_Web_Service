from fastapi import APIRouter, Header, status, Path
from fastapi.responses import JSONResponse
from app.api.schemas.catalogo_schema import (
    ServicioCreate, ServicioResponse, ServicioDataResponse, 
    CatalogoResponse, ServicioCatalogoItem,
    ModalidadUpdate, ModalidadResponse, ModalidadDataResponse
)
from app.services.services.catalogo_service import catalogo_service

# API Catálogo: Agrupa HU-026, HU-029 y HU-031
router = APIRouter(prefix="/api/v1/catalogo", tags=["Catálogo"])

# --- HU-029: Consultar Catálogo ---
@router.get("", response_model=CatalogoResponse, status_code=status.HTTP_200_OK)
def consultar_catalogo():
    try:
        servicios_activos = catalogo_service.obtener_catalogo()
        
        if not servicios_activos:
            return CatalogoResponse(mensaje="No hay servicios disponibles en este momento", data=[], success=True)
            
        data_items = [
            ServicioCatalogoItem(
                id_servicio=s.id_servicio, nombre=s.nombre, precio=s.precio,
                duracion_minutos=s.duracion_minutos, aplica_domicilio=s.aplica_domicilio
            ) for s in servicios_activos
        ]
        
        return CatalogoResponse(message="Catálogo consultado exitosamente", data=data_items, success=True)
        
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"mensaje": "Error al intentar recuperar el catálogo de servicios.", "data": None, "success": False}
        )

# --- HU-026: Crear Servicio ---
@router.post("/servicios", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def registrar_servicio(
    payload: ServicioCreate,
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador'")
):
    try:
        servicio_creado = catalogo_service.crear_servicio(payload, x_rol_usuario)
        return ServicioResponse(
            message="Servicio registrado exitosamente",
            data=ServicioDataResponse(id_servicio=servicio_creado.id_servicio, nombre=servicio_creado.nombre, estado=servicio_creado.estado),
            success=True
        )
    except FileExistsError as e:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"mensaje": str(e), "data": None, "success": False})
    except PermissionError as e:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"mensaje": str(e), "data": None, "success": False})
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"mensaje": str(e), "data": None, "success": False})

# --- HU-031: Habilitar Domicilio ---
@router.patch("/servicios/{id}/modalidad", response_model=ModalidadResponse, status_code=status.HTTP_200_OK)
def habilitar_domicilio(
    payload: ModalidadUpdate,
    id: int = Path(..., description="ID del servicio a modificar"),
    x_rol_usuario: str = Header(default="Administrador", description="Enviar 'Administrador' o 'Cliente' para probar permisos")
):
    try:
        # Llamada a la capa de servicio
        servicio_actualizado = catalogo_service.actualizar_modalidad(id, payload, x_rol_usuario)
        
        # Caso 1 y 3: Éxito
        return ModalidadResponse(
            message="Modalidad de servicio actualizada exitosamente",
            data=ModalidadDataResponse(
                id_servicio=servicio_actualizado.id_servicio,
                aplica_domicilio=servicio_actualizado.aplica_domicilio
            ),
            success=True
        )
        
    except KeyError as e:
        # Caso 2: El servicio no existe (HTTP 404 Not Found)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mensaje": str(e).strip("'"), "data": None, "success": False} # strip("'") limpia las comillas de KeyError
        )
    except PermissionError as e:
        # Caso 4: Permisos insuficientes (HTTP 403 Forbidden)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"mensaje": str(e), "data": None, "success": False}
        )
    except Exception:
        # Caso 5: Fallo general simulado de BD (HTTP 503)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"mensaje": "Error al actualizar la modalidad del servicio.", "data": None, "success": False}
        )
