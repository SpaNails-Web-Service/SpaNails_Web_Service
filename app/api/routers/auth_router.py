from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.api.schemas.auth_schema import LoginRequest, LoginResponse
from app.services.services.auth_service import auth_service

# API Auth: Endpoint para inicio de sesión
router = APIRouter(prefix="/api/v1/usuarios", tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest):
    try:
        # 1. Llamada a la capa de servicio
        login_data = auth_service.autenticar_usuario(payload)
        
        # 2. Caso de éxito (HTTP 200 OK)
        return LoginResponse(
            message="Inicio de sesión exitoso",
            data=login_data,
            success=True
        )
        
    except PermissionError as e:
        # 3. Casos de error de credenciales o inactividad (HTTP 401 Unauthorized)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
    except ValueError as e:
        # 4. Caso de validación (Ej. Contraseña vacía) (HTTP 400 Bad Request)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": str(e),
                "data": None,
                "success": False
            }
        )
