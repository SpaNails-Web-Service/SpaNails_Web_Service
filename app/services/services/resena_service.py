from fastapi import HTTPException, status
from app.repositories.repositories.resena_repository import ResenaRepository

class ResenaService:
    def __init__(self, repository: ResenaRepository):
        self.repository = repository

    def publicar_resena(self, id_cita: int, calificacion: int, comentario: str):
        # Validar rango de calificación
        if not (1 <= calificacion <= 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "La calificación debe estar entre 1 y 5 estrellas",
                    "data": None,
                    "success": False
                }
            )

        # Validar existencia y estado de la cita ("Finalizado" o "Completado")
        cita = self.repository.obtener_cita_por_id(id_cita)
        
        # Validación de negocio (ajustar según el estado real de la BD)
        estado_valido = True  # Cambiar por la validación de tu modelo de cita
        estado_actual = "Completado"

        if not estado_valido or estado_actual not in ["Finalizado", "Completado"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "mensaje": "No es posible reseñar un servicio que no ha sido completado",
                    "data": None,
                    "success": False
                }
            )

        resena = self.repository.guardar_resena(id_cita, calificacion, comentario)

        return {
            "message": "Reseña publicada con éxito",
            "data": {
                "id_resena": resena["id_resena"],
                "calificacion": resena["calificacion"]
            },
            "success": True
        }