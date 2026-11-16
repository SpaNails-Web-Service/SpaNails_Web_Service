from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.Direccion_schema import DireccionCreate, DireccionResponse
from app.api.dependencies.auth import obtener_cliente_actual
from app.services.services.direccion_service import direccion_service
from database import get_db

router = APIRouter()

@router.post("/api/v1/usuarios/direcciones", response_model=DireccionResponse, status_code=201)
def añadir_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(obtener_cliente_actual),
):
    return direccion_service.crear_direccion(
        db=db,
        usuario_id=user_id,
        direccion_in=direccion,
    )
