from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.repositories.database import get_db
from app.api.schemas.resena_schema import ResenaCreate, ResenaResponse
from app.repositories.repositories.resena_repository import ResenaRepository
from app.services.services.resena_service import ResenaService

router = APIRouter(prefix="/api/v1", tags=["Reseñas"])

@router.post(
    "/resenas",
    response_model=ResenaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publicar reseña con validación"
)
def publicar_resena(resena_data: ResenaCreate, db: Session = Depends(get_db)):
    repo = ResenaRepository(db)
    service = ResenaService(repo)
    return service.publicar_resena(
        id_cita=resena_data.id_cita,
        calificacion=resena_data.calificacion,
        comentario=resena_data.comentario
    )
