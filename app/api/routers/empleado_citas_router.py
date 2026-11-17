from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.schemas.empleado_citas_schema import EmpleadoCitasRespuesta
from app.services.services.empleado_citas_service import EmpleadoCitasService
from app.repositories.repositories.empleado_citas_repository import EmpleadoCitasRepository
from database import get_db

repo = EmpleadoCitasRepository()
service = EmpleadoCitasService(repo)

router = APIRouter(prefix="/api/v1/empleados", tags=["Empleados - Agenda"])

# Dependencia simulada de autenticación por Token (ajusta con la real de tu equipo si la tienes)
def obtener_empleado_actual():
    # En producción esto vendría del token JWT decodificado
    return {"id": 5, "roles": ["Manicurista"], "activo": True}

@router.get(
    "/citas",
    response_model=EmpleadoCitasRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Visualizar citas manicurista",
    description="Permite a la manicurista autenticada visualizar sus citas asignadas y retornar los IDs de seguimiento."
)
def visualizar_citas_manicurista(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_empleado_actual)
):
    try:
        return service.obtener_agenda_manicurista(db=db, usuario_actual=usuario_actual)
    
    except HTTPException as http_exc:
        # Propagar excepciones HTTP controladas (como el 403 Forbidden)
        raise http_exc

    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "mensaje": "Error de conexión con la base de datos de citas",
                "data": [],
                "success": False
            }
        )