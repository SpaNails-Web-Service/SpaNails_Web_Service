from fastapi import APIRouter, HTTPException, status
from app.api.schemas.cliente_schema import ClienteCreate, ClienteResponse, ClienteDataResponse
from app.services.services.cliente_service import cliente_service

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

@router.post("/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(payload: ClienteCreate):
    try:
        # 1. Llamada a la capa de servicio
        cliente_creado = cliente_service.crear_cliente(payload)
        
        # 2. Mapeo exitoso (Código 201)
        return ClienteResponse(
            message="Cliente registrado exitosamente",
            data=ClienteDataResponse(
                id_cliente=cliente_creado.id_cliente,
                email=cliente_creado.email,
                fecha_registro=cliente_creado.fecha_registro
            ),
            success=True
        )
        
    except ValueError as e:
        # 3. Mapeo de errores de negocio (Código 400)
        # Se estructura exactamente como el "Caso 2" de la HU
        return ClienteResponse(
            message=str(e),
            data=ClienteDataResponse(
                id_cliente=0,
                email="",
                fecha_registro="1970-01-01" # Fecha por defecto para mantener el tipo de dato
            ),
            success=False
        )