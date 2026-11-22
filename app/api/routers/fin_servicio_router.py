from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.schemas.fin_servicio_schema import ViajeFinalizarCreate, ViajeRespuesta
from app.services.services.fin_servicio_service import ViajeService
from app.repositories.repositories.fin_servicio_repository import ViajeRepository
from database import get_db

repo = ViajeRepository()
service = ViajeService(repo)

router = APIRouter(prefix="/api/v1/logistica", tags=["Logística - Finalizar Servicio"])

def get_current_user():
    return {"id": 10, "roles": ["Domiciliario"], "activo": True}

@router.post(
    "/viajes/{id_viaje}/finalizar",
    response_model=ViajeRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Finalizar servicio logístico",
    description="Permite al domiciliario asignado o administrador finalizar el servicio logístico actualizando su estado."
)
def finalizar_servicio_logistico(
    id_viaje: int,
    datos: ViajeFinalizarCreate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user)
):
    try:
        if not usuario_actual.get("activo"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado o inactivo"
            )
        
        return service.finalizar_viaje(db=db, id_viaje=id_viaje, datos=datos, usuario_actual=usuario_actual)

    except SQLAlchemyError:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "Service Unavailable: Falla en la conexión a la base de datos",
                "data": None,
                "success": False
            }
        )