from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.Direccion_schema import DireccionCreate, DireccionResponse 
from app.services.direccion_service import direccion_service
from app.repositories.database import get_db

router = APIRouter()

def get_current_user(): 
    return {"id": 1, "activo": True}

@router.post("/api/v1/usuarios/direcciones", response_model=DireccionResponse, status_code=201)
def añadir_direccion(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user.get("activo"):
        raise HTTPException(status_code=403, detail="El usuario no tiene una cuenta activa")

    # Llamamos al método desde la instancia de la clase
    return direccion_service.crear_direccion(
        db=db, 
        usuario_id=current_user["id"], 
        direccion_in=direccion
    )