from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse
from app.api.schemas.admin_schema import AdminCreate, AdminResponse, AdminDataResponse
from app.services.services.admin_service import admin_service

# Mantenemos la ruta base para cumplir el endpoint exigido
router = APIRouter(prefix="/api/v1/usuarios", tags=["Administradores"])

@router.post("/administradores", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def registrar_administrador(
    payload: AdminCreate, 
    # Cabecera simulada para probar los permisos de la HU sin JWT real aún
    x_rol_usuario: str = Header(default="Gerente", description="Enviar 'Gerente' o 'Cliente' para probar permisos")
):
    try:
        admin_creado = admin_service.crear_admin(payload, x_rol_usuario)
        
        # Caso de éxito
        return AdminResponse(
            message="Administrador creado exitosamente",
            data=AdminDataResponse(
                id_admin=admin_creado.id_admin,
                rol=admin_creado.rol_nombre
            ),
            success=True
        )
        
    except PermissionError as e:
        # Caso 2 de prueba: Sin privilegios (Error 403)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
        
    except ValueError as e:
        # Caso 4 de prueba: Rol paramétrico inválido (Error 400)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )