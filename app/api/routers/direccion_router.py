from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import obtener_cliente_actual
from app.api.schemas.direccion_schema import DireccionCreate, DireccionResponse
from app.services.services.direccion_service import direccion_service
from database import get_db

router = APIRouter(prefix="/api/v1/usuarios", tags=["Direcciones"])


@router.post(
    "/direcciones",
    response_model=DireccionResponse,
    status_code=status.HTTP_201_CREATED,
)
def añadir_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(obtener_cliente_actual),
):
    return direccion_service.crear_direccion(
        db=db,
        usuario_id=usuario_id,
        direccion_in=direccion,
    )