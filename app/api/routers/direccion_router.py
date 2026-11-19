from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemas.direccion_schema import DireccionCreate, DireccionResponse 
from app.services.services.direccion_service import direccion_service
from database import get_db

# Definimos el prefijo general para las rutas de direcciones de usuarios
router = APIRouter(prefix="/api/v1/usuarios", tags=["Direcciones"])

def get_current_user(): 
    # Simulación temporal de usuario autenticado
    return {"id": 1, "activo": True}

@router.post("/direcciones", response_model=DireccionResponse, status_code=status.HTTP_201_CREATED)
def añadir_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validar que el usuario de la sesión esté activo
    if not current_user.get("activo"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="El usuario no tiene una cuenta activa"
        )

    # Invocamos la lógica orientada a objetos desde el servicio de direcciones
    return direccion_service.crear_direccion(
        db=db, 
        usuario_id=current_user["id"], 
        direccion_in=direccion
    )