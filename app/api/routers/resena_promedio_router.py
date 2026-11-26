from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.dependencies import get_db # Dependencia de tu base de datos
from app.api.schemas.resena_promedio_schema import ResenaPromedioResponse
from app.services.services.resena_promedio_service import ResenaPromedioService
from datetime import datetime

router = APIRouter(prefix="/api/v1/resenas", tags=["Reseñas - Catálogo Público"])

@router.get("/promedio", response_model=None, status_code=status.HTTP_200_OK)
def calcular_calificacion_promedio(
    fecha: Optional[str] = Query(None, description="Filtro opcional de fecha"),
    db: Session = Depends(get_db)
):
    # Caso 4: Parámetros de filtro inválidos enviados en Query String (?fecha=invalida)
    if fecha is not None:
        try:
            # Intentamos validar formato de fecha básico (ej. YYYY-MM-DD)
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha inválido en los parámetros de consulta."
            )
            
    resultado = ResenaPromedioService.calcular_promedio_resenas(db)
    return resultado