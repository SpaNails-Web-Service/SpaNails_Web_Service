from sqlalchemy.orm import Session
from app.repositories.repositories.resena_promedio_repository import ResenaPromedioRepository

class ResenaPromedioService:
    @staticmethod
    def calcular_promedio_resenas(db: Session):
        promedio_bruto, total_resenas = ResenaPromedioRepository.obtener_datos_promedio(db)
        
        # Caso 2: Si no hay reseñas registradas aún
        if total_resenas == 0:
            return {
                "mensaje": "Aún no hay calificaciones suficientes",
                "data": {
                    "promedio_global": 0.0,
                    "total_resenas": 0
                },
                "success": True
            }
            
        # Criterio de Aceptación 1: Redondear a un máximo de 1 decimal
        promedio_redondeado = round(promedio_bruto, 1)
        
        return {
            "message": "Cálculo de promedio exitoso",
            "data": {
                "promedio_global": promedio_redondeado,
                "total_resenas": total_resenas
            },
            "success": True
        }