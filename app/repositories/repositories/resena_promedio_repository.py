from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.domain.models.resena_model import ResenaModel 

class ResenaPromedioRepository:
    @staticmethod
    def obtener_datos_promedio(db: Session):
        try:
            # Consultamos el total de reseñas y el promedio de la columna calificacion
            total_resenas = db.query(func.count(ResenaModel.id)).scalar() or 0
            
            if total_resenas == 0:
                return 0.0, 0
                
            promedio = db.query(func.avg(ResenaModel.calificacion)).scalar() or 0.0
            
            return float(promedio), int(total_resenas)
        except Exception as e:
            # Caso 5: Falla la base de datos al realizar la agregación (SUM/AVG) -> HTTP 503
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error de conexión o fallo en la base de datos al calcular el promedio"
            )
